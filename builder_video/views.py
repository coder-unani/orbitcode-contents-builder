import json
from urllib.request import urlopen
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .parsers import NetflixParser
from .query import create_content_data
from .properties import (
    URL_NETFLIX_LOGIN, 
    URL_NETFLIX_CONTENT, 
    AWS_S3_NETFLIX_THUMBNAIL, 
    LOCAL_NETFLIX_THUMBNAIL
)


# Create your views here.
def index(request):
    return render(request, "builder/video/index.html")

class NetflixView(ListView):
    def __init__(self):
        self.template_name = "builder/video/netflix/index.html"

    def get_content_netflix(self, search_id):
        url = URL_NETFLIX_CONTENT + search_id
        with urlopen(url) as response:
            html = response.read()
        # BeautySoup을 이용하여 데이터 파싱
        if html:
            bs4 = NetflixParser(html=html)
            content = bs4.parse_content_netflix()
            content['platform_id'] = search_id
            content['watchs'] = [
                {"kind": "11", "url": URL_NETFLIX_CONTENT + search_id}
            ]
            bs4.close()
            return content
        else:
            return None

    def make_correct_content(self, content, content_id=None, content_kind=None):
        new_content = content
        # platform_id & watchs 보정
        if content_id is not None:
            new_content['platform_id'] = content_id
            new_content['watchs'][0]['url'] = URL_NETFLIX_CONTENT + content_id
        
        # video kind
        if content_kind is not None:
            if content_kind == "movie":
                new_content['kind'] = "10"
            elif content_kind == "series":
                new_content['kind'] = "11"
            else:
                new_content['kind'] = "99"
            
        return new_content

    def get(self, request):

        search_ids = request.GET.get('search_ids')
        context = dict()
        
        if search_ids:
            search_ids_to_list = search_ids.split(',')
            content_ids = []
            contents = []
        
            for search_id in search_ids_to_list:
                content = self.get_content_netflix(search_id)
                if content:
                    content_ids.append(search_id)
                    contents.append(content)
            
            context['content_ids'] = content_ids
            context['contents'] = contents
        
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request):

        content_ids = request.POST.get('content_ids')

        content_ids_to_list = content_ids.split(',')
        for content_id in content_ids_to_list:
            content = request.POST.get('content_' + content_id)
            content_kind = request.POST.get('content_kind_' + content_id)
            
            content_to_dict = eval(content)

            new_content = self.make_correct_content(content_to_dict, content_id, content_kind)
            
            if create_content_data(new_content):
                print("Success")
            else:
                print("Fail")
            
        return render(request, template_name=self.template_name)
    



