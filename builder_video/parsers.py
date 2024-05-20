from bs4 import BeautifulSoup

class BeautySoupParser:
    def __init__(self, html=None, parser="html.parser"):
        self._parser = parser
        if html is not None:
            self._soup = BeautifulSoup(html, parser)
        
    def get_element(self, tag, classname=None, attrs=None):
        result = None
        if classname is not None and attrs is not None:
            result = self._soup.find(tag, class_=classname, attrs=attrs)
        elif classname is not None:
            result = self._soup.find(tag, class_=classname)
        elif attrs is not None:
            result = self._soup.find(tag, attrs=attrs)    
        return result
    
    def get_elements(self, tag, classname=None, attrs=None):
        result = []
        if classname is not None and attrs is not None:
            result = self._soup.find_all(tag, class_=classname, attrs=attrs)
        elif classname is not None:
            result = self._soup.find_all(tag, class_=classname)
        elif attrs is not None:
            result = self._soup.find_all(tag, attrs=attrs)
        return result

    def close(self):
        self._soup.decompose()

class NetflixParser(BeautySoupParser):
    def __init__(self, html=None):
        super().__init__(html)
    
    def parse_content_netflix(self):        
        schema = self.get_element(tag="script", attrs={"type": "application/ld+json"})
        schema = schema.text.strip()
        schema_to_dict = eval(schema)

        content = dict()
        # type 추출
        content['type'] = "" 
        if schema_to_dict['@type'] == "Movie":
            content['type'] = "10"
        elif schema_to_dict['@type'] == "TVSeries":
            content['type'] = "11"
        content['title'] = schema_to_dict['name'] # title 추출
        content['synopsis'] = schema_to_dict['description'] # synopsis 추출
        content['platform_code'] = "10" # Netflix platform_code
        content['platform_id'] = schema_to_dict['url'].split("/")[-1] # platform_id 추출
        content['notice_age'] = schema_to_dict['contentRating'] # 연령고지 추출
        # Thumbnail 이미지 추출
        content['thumbnails'] = [
            {"type": "11", "thumbnail": schema_to_dict['image'], "extension": "", "size": 0}
        ]
        # watch url 추출
        content['watchs'] = [
            {"type": "10", "url": schema_to_dict['url']}  
        ]
        # 장르 추출
        content['genres'] = []
        genres = self.get_elements(tag="a", classname="item-genres")
        for genre in genres:
            content['genres'].append({"name": genre.text.strip()})
        # 출연진 추출
        content['actors'] = []
        actor_count = 0
        for actor in schema_to_dict['actors']:
            type = "10"
            if actor_count > 1:
                type = "11"
            content['actors'].append({"type": type, "name": actor['name'], "role": "", "picture": "", "profile": ""})
            actor_count += 1
        # 제작진 초기화
        content['staffs'] = []
        # 감독 추출
        for director in schema_to_dict['director']:
            content['staffs'].append({"type": "10", "name": director['name'], "picture": "", "profile": ""})
        # 제작진 추출
        for creator in schema_to_dict['creator']:
            content['staffs'].append({"type": "11", "name": creator['name'], "picture": "", "profile": ""})
        # 파싱 범위 축소
        self._soup = self.get_element(tag="div", classname="hero-container")
        # release 추출
        content['release'] = self.get_element(tag="span", classname="item-year")
        if content['release'] is not None:
            content['release'] = content['release'].text.strip()
        # 상영시간 추출
        content['runtime'] = self.get_element(tag="span", classname="item-runtime", attrs={"data-uia": "item-runtime"})
        if content['runtime'] is not None:
            content['runtime'] = content['runtime'].text.strip()
        
        print(content)
        return content