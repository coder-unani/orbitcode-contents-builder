import os
import json
from datetime import datetime
from urllib.request import urlopen
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .parsers import NetflixParser
from .query import create_content_data
from .utils import make_filename, save_file_from_url, get_file_extension, get_file_size
from .s3client import S3Client
from .properties import (
    URL_NETFLIX_LOGIN, 
    URL_NETFLIX_CONTENT, 
    AWS_S3_NETFLIX_THUMBNAIL, 
    LOCAL_NETFLIX_THUMBNAIL
)

DJANGO_LOGIN_URL = "/account/login/"
DJANGO_REDIRECT_FIELD_NAME = "next"

# Create your views here.
def index(request):
    return render(request, "builder/video/index.html")

class NetflixFindView(LoginRequiredMixin, ListView):
    # login_url = reverse("account:login")
    login_url = DJANGO_LOGIN_URL
    redirect_field_name = DJANGO_REDIRECT_FIELD_NAME
    template_name = "builder/video/netflix/index.html"

    def get(self, request):

        search_ids = request.GET.get('search_ids')
        context = dict()
        
        if search_ids:
            search_ids_to_list = search_ids.split(',')
            content_ids = []
            contents = []
            parser = NetflixParser()
            for search_id in search_ids_to_list:
                content = parser.get_content_netflix(search_id)
                if content:
                    content_ids.append(search_id)
                    contents.append(content)
            parser.close()
            
            context['content_ids'] = content_ids
            context['contents'] = contents
        
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request):

        content_ids = request.POST.get('content_ids')

        content_ids_to_list = content_ids.split(',')
        for content_id in content_ids_to_list:
            content = eval(request.POST.get('content_' + content_id))
            
            if create_content_data(content):
                print("Success")
            else:
                print("Fail")
            
        return render(request, template_name=self.template_name)

    
class NetflixBoxOfficeView(LoginRequiredMixin, ListView):
    login_url = DJANGO_LOGIN_URL
    redirect_field_name = DJANGO_REDIRECT_FIELD_NAME
    template_name = "builder/video/netflix/boxoffice.html"
    contents_file = "data/netflix/boxoffice/{}_{}_{}_{}_{}.json".format("10", datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour)

    def get(self, request):
        # scrap == on 데이터 파싱 시작
        parser = request.GET.get('parser')
        view_mode = "html"

        if parser == "on":
            if request.GET.get('view_mode'):
                view_mode = request.GET.get('view_mode')
            
            # 파일에서 컨텐츠 로드
            contents = self.load_contents_from_file()

            # 파일이 없으면 넷플릭스 파싱
            if contents is None:
                parser = NetflixParser()
                contents = parser.get_most_watched()
                # 가져온 컨텐츠를 파일에 저장
                self.save_contents_to_file(contents)
            
            # contents 분리
            content_ids = []
            movies = []
            series = []
            for content in contents:
                content_ids.append(content['platform_id'])
                if content['type'] == "10":
                    movies.append(content)
                elif content['type'] == "11":
                    series.append(content)            
            movies = sorted(movies, key=lambda x: x['rank'])
            series = sorted(series, key=lambda x: x['rank'])
            
            # context 생성
            context = {
                "view_mode": view_mode,
                "parser": parser,
                "content_ids": ",".join(content_ids),
                "contents": {
                    "movies": movies,
                    "series": series
                }
            }

            # 화면 출력
            return render(request, template_name=self.template_name, context=context)
            
        else:
            # 화면 출력
            return render(request, template_name=self.template_name)
            
    def post(self, request):
        
        content_ids = request.POST.get('content_ids')
        content_ids_to_list = content_ids.split(',')
        for content_id in content_ids_to_list:
            content = eval(request.POST.get('content_' + content_id))

            # s3 client 생성
            s3client = S3Client()

            # 썸네일 로컬 저장, S3 업로드 처리, 썸네일 URL 변경
            thumbnails = content['thumbnails']
            for i in range(len(thumbnails)):    
                # Thumbnail info
                file_url = thumbnails[i]['thumbnail']
                file_name = make_filename(file_url)
                file_path = os.path.join(LOCAL_NETFLIX_THUMBNAIL, file_name)
                # local Thumbnail save
                if save_file_from_url(file_url, file_path):
                    thumbnails[i]['thumbnail'] = os.path.join(AWS_S3_NETFLIX_THUMBNAIL, file_name)
                    thumbnails[i]['extension'] = get_file_extension(file_name)
                    thumbnails[i]['size'] = get_file_size(file_path)
                    # Thumbnail s3 upload
                    s3_thumbnail_file = s3client.upload_file(file_path, AWS_S3_NETFLIX_THUMBNAIL)
                    if not s3_thumbnail_file:
                        print("Thumbnail upload fail")
                        continue
            s3client.close()

            # Thumbnail Update
            content['thumbnails'] = thumbnails

            # Database Insert
            if create_content_data(content):
                print("Success")
            else:
                print("Fail")

        # 화면 출력
        return render(request, self.template_name)

    def load_contents_from_file(self):
        # 파일이 존재하는지 확인
        if os.path.isfile(self.contents_file):
            loaded_data = ""
            # json 파일 불러오기
            with open(self.contents_file, "r") as file:
                loaded_data = json.load(file)

            contents = loaded_data['contents']
            if len(contents) > 0 or contents is not None:
                return contents
            else:
                return None
        else:
            return None

    def save_contents_to_file(self, contents):
        if len(contents) > 0:
            with open(self.contents_file, "w") as file:
                json.dump(obj={"contents": contents}, fp=file, indent=4)
            return True
        else:
            return False
        

class NetflixDetailView(LoginRequiredMixin, DetailView):
    login_url = DJANGO_LOGIN_URL
    redirect_field_name = DJANGO_REDIRECT_FIELD_NAME
    template_name = "builder/video/netflix/index.html"

    def get(self, request, pk):
        content = self.get_content_netflix(pk)
        context = dict()
        context['content'] = content
        return render(request, template_name=self.template_name, context=context)