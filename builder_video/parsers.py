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
            result = self._soup.find_all(tag, class_=classname)
        elif classname is not None:
            result = self._soup.find(tag, class_=classname)
        elif attrs is not None:
            result = self._soup.find(tag, attrs=attrs)
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
        content['title'] = schema_to_dict['name'] # title 추출
        content['synopsis'] = schema_to_dict['description'] # synopsis 추출
        content['platform_code'] = "10" # Netflix platform_code
        content['platform_id'] = schema_to_dict['url'].split("/")[-1] # platform_id 추출
        content['notice_age'] = schema_to_dict['contentRating'] # 연령고지 추출
        
        # Thumbnail 이미지 추출
        content['thumbnails'] = [
            {"kind": "11", "thumbnail": schema_to_dict['image'], "extension": "", "size": 0}
        ] 
        # watch url 추출
        content['watchs'] = [
            {"kind": "10", "url": schema_to_dict['url']}  
        ]
        # 장르 추출
        content['genres'] = []
        content['genres'].append({"name": schema_to_dict['genre']})


        # Cover 이미지 추출
        # self._soup = self.get_element(tag="div", classname="hero-container")
        # hero_image_desktop = self.get_element(tag="div", classname="hero-image-desktop")
        # hero_image_desktop = hero_image_desktop['style'].split("url(")[1].split(")")[0].replace("\"", "")
        # hero_image_mobile = self.get_element(tag="div", classname="hero-image-mobile")
        # hero_image_mobile = hero_image_mobile['style'].split("url(")[1].split(")")[0].replace("\"", "")

        # 컨텐츠 상세정보 추출
        # self._soup = self.get_element(tag="div", classname="details-container")
        
        # title 추출
        # title = self.get_element(tag="h1", classname="title-title")
        # if title is not None:
        #     title = title.text.strip()
        
        # synopsis 추출
        # synopsis = self.get_element(tag="div", classname="title-info-synopsis")
        # if synopsis is not None:
        #     synopsis = synopsis.text.strip()

        # release 추출
        release = self.get_element(tag="span", classname="item-year")
        if release is not None:
            release = release.text.strip()

        # 상영시간 추출
        runtime = self.get_element(tag="span", classname="item-runtime", attrs={"data-uia": "item-runtime"})
        if runtime is not None:
            runtime = runtime.text.strip()
        
        # 비디오 kind 보정

        # 연령고지 추출
        # notice_age = self.get_element(tag="span", classname="maturity-number")
        # if notice_age is not None:
        #     notice_age = notice_age.text.strip()

        # 장르 추출
        # genres = []
        # genre = self.get_element(tag="a", classname="item-genre", attrs={"data-uia": "item-genre"})
        # if genre is not None:
        #     genre = genre.text.strip()
        #     genre_to_list = genre.split(",")

        #     for i in range(len(genre_to_list)):
        #         genres.append({"name": genre_to_list[i]})
        
        # 출연진 추출
        casts = []
        cast = self.get_element(tag="span", classname="title-data-info-item-list", attrs={"data-uia": "info-starring"})
        if cast is not None:
            cast = cast.text.strip()
            cast_to_list = cast.split(",")

            for i in range(len(cast_to_list)):
                if i <= 1:
                    kind = "10"
                else: 
                    kind = "11"
                casts.append({"kind": kind, "name": cast_to_list[i], "role": "", "picture": "", "profile": ""})

        # 제작진 추출
        staffs = []
        staff = self.get_element(tag="span", classname="title-data-info-item-list", attrs={"data-uia": "info-creators"})
        if staff is not None:
            staff = staff.text.strip()
            staff_to_list = staff.split(",")
        
            for i in range(len(staff_to_list)):
                if i == 0:
                    kind = "10"
                else: 
                    kind = "11"
                staffs.append({"kind": kind, "name": staff_to_list[i], "role":"", "picture": "", "profile": ""})

        # 컨텐츠 링크 추출
        watchs = [
            {"kind": "10", "url": watch_url}   
        ]

        # Thumbnail 이미지 추출
        thumbnails = [
            {"kind": "11", "thumbnail": hero_image_desktop, "extension": "", "size": 0},
            {"kind": "12", "thumbnail": hero_image_mobile, "extension": "", "size": 0},
        ]
        
        result = {
            "kind": "",
            "title": title,
            "synopsis": synopsis,
            "release": release,
            "runtime": runtime,
            "notice_age": notice_age,
            "genres": genres,
            "casts": casts,
            "staffs": staffs,
            "platform_code": "10", # "10": "netflix
            "platform_id": platform_id,
            "watchs": watchs,
            "thumbnails": thumbnails,
            "is_db": "N"
        }

        return result