import os
import json
from datetime import datetime
from urllib.request import urlopen
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers

from .parsers import NetflixParser
from .query import create_content_data, exist_content_video, get_video, create_video_thumbnail
from .utils import make_filename, save_file_from_url, get_file_extension, get_file_size
from .logger import info_log, error_log
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

    def get(self, request, **kwargs):

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
    path_file = "data/netflix/"
    path_file_contents = path_file + "contents_{}_{}_{}_{}.json".format(
        datetime.now().year,
        datetime.now().month,
        datetime.now().day,
        datetime.now().hour
    )
    path_file_ranks = path_file + "ranks_{}_{}_{}_{}.json".format(
        datetime.now().year,
        datetime.now().month,
        datetime.now().day,
        datetime.now().hour
    )

    def get(self, request, **kwargs):
        # scrap == on 데이터 파싱 시작
        parser = request.GET.get('parser')
        view_mode = "html"

        if parser == "on":
            info_log(self.__class__.__name__, "START. Netflix box office data parsing. parser={}, view_mode={}".format(parser, view_mode))

            if request.GET.get('view_mode'):
                view_mode = request.GET.get('view_mode')

            # 파일에서 컨텐츠 로드
            contents = self.load_from_file(self.path_file_contents)
            ranks = self.load_from_file(self.path_file_ranks)

            # 파일이 없으면 넷플릭스 파싱
            if contents is None or ranks is None:
                parser = NetflixParser()
                contents, ranks = parser.get_contents()
                parser.close()
                # contents 가져오기
                parse_contents = []
                for content in contents:
                    if exist_content_video(platform_id=content['platform_id']):
                        # TODO: 이미 존재하는 컨텐츠 DB에 있는데 데이터 불러오기
                        continue
                    parser = NetflixParser()
                    url = URL_NETFLIX_CONTENT + "/" + content['platform_id']
                    with urlopen(url) as response:
                        html = response.read()
                    new_content = parser.parse_content(html)
                    parser.close()
                    print("=============================================================================")
                    print(content)
                    print(new_content)
                    if content.get('thumbnail') and new_content.get('thumbnail'):
                        new_content['thumbnail'].append(content['thumbnail'])
                    parse_contents.append(new_content)
                contents = parse_contents
                parser.close()
                # 가져온 컨텐츠를 파일에 저장
                self.save_to_file(self.path_file_contents, contents)
                self.save_to_file(self.path_file_ranks, ranks)

            # contents 분리
            content_ids = []
            rank_movies = []
            rank_series = []

            for rank in ranks:
                if rank['type'] == "10":
                    rank_movies.append(rank)
                elif rank['type'] == "11":
                    rank_series.append(rank)
            movies = sorted(rank_movies, key=lambda x: x['rank'])
            series = sorted(rank_series, key=lambda x: x['rank'])

            for content in contents:
                content_ids.append(content['platform_id'])
            
            # context 생성
            context = {
                "view_mode": view_mode,
                "parser": parser,
                "content_ids": ",".join(content_ids),
                "ranks": {
                    "movies": movies,
                    "series": series
                },
                "contents": contents
            }

            info_log(self.__class__.__name__, "END. Netflix box office data parsing")
            # 화면 출력
            return render(request, template_name=self.template_name, context=context)
            
        else:
            # 화면 출력
            return render(request, template_name=self.template_name)
            
    def post(self, request):
        
        info_log(self.__class__.__name__, "START. Save Netflix box office data to database.")

        content_ids = request.POST.get('content_ids')
        content_ids_to_list = content_ids.split(',')
        for content_id in content_ids_to_list:
            content = eval(request.POST.get('content_' + content_id))

            if exist_content_video(platform_id=content['platform_id']):
                info_log(self.__class__.__name__, "Already exist. platform_id={}".format(content['platform_id']))
                continue

            # Database creation
            video = create_content_data(content)
            if video:
                thumbnails = video.thumbnail.all()
                s3client = S3Client()
                for thumbnail in thumbnails:
                    file_name = make_filename(thumbnail.url)
                    file_path = os.path.join(LOCAL_NETFLIX_THUMBNAIL, file_name)
                    if not save_file_from_url(thumbnail.url, file_path):
                        continue
                    if not s3client.upload_file(file_path, AWS_S3_NETFLIX_THUMBNAIL):
                        continue
                    thumbnail.url = os.path.join(AWS_S3_NETFLIX_THUMBNAIL, file_name)
                    thumbnail.extension = get_file_extension(file_name)
                    thumbnail.size = get_file_size(file_path)
                    thumbnail.save()
                s3client.close()
                
        info_log(self.__class__.__name__, "END. Save Netflix box office data to database.")

        context = {
            "message": "넷플릭스 박스오피스 데이터를 저장하였습니다."
        }
        # 화면 출력
        return render(request, self.template_name, context=context)

    def load_from_file(self, path_file):
        try:
            with open(path_file, "r") as file:
                contents = json.load(file)
            if len(contents) > 0 or contents is not None:
                info_log(self.__class__.__name__, "Load from file successful. file={}".format(path_file))
            else:
                error_log(self.__class__.__name__, "Failed to load from file. file={}".format(path_file))
            return contents
        except Exception as e:
            error_log(self.__class__.__name__, "Failed to load from file. file={}, error={}".format(path_file, e))
            return None

    def save_to_file(self, path_file, content):
        try:
            with open(path_file, "w") as file:
                json.dump(obj=content, fp=file, indent=4)
            info_log(self.__class__.__name__, "Save to file success. file={}".format(self.path_file))
            return True
        except Exception as e:
            error_log(self.__class__.__name__, "Failed to save to file. file={} / e={}".format(self.path_file, e))
            return False


class NetflixDetailView(LoginRequiredMixin, DetailView):
    login_url = DJANGO_LOGIN_URL
    redirect_field_name = DJANGO_REDIRECT_FIELD_NAME
    template_name = "builder/video/netflix/detail.html"

    def get(self, request, pk, *args, **kwargs):

        video = get_video(pk)

        thumbnails = list()
        s3client = S3Client()
        for thumbnail in video.thumbnail.all():
            presigned_url = s3client.create_presigned_url(thumbnail.url)
            thumbnails.append({
                "type": thumbnail.type,
                "url": thumbnail.url,
                "extension": thumbnail.extension,
                "size": thumbnail.size,
                "presigned_url": presigned_url
            })
        s3client.close()
        thumbnails = sorted(thumbnails, key=lambda x: x['type'])

        video_dict = dict()
        video_dict = {
            "id": video.id,
            "platform_id": video.platform_id,
            "title": video.title,
            "type": video.type,
            "synopsis": video.synopsis,
            "grade": video.grade,
            "runtime": video.runtime,
            "release": video.release,
            "created_at": video.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": video.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "thumbnail": thumbnails,
            "watch": serializers.serialize(format="json", queryset=video.watch.all()),
            "actor": serializers.serialize(format="json", queryset=video.actor.all()),
            "staff": serializers.serialize(format="json", queryset=video.staff.all()),
            "genre": serializers.serialize(format="json", queryset=video.genre.all()),
        }
        json1 = json.dumps(video_dict)
        print(json1)

        context = dict()
        context = {
            "content": video,
            "thumbnails": thumbnails
        }

        return render(request, template_name=self.template_name, context=context)
    