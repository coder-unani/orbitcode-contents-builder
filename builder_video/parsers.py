from time import sleep
from urllib.request import urlopen
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from .utils import html_escape
from .properties import (
    URL_NETFLIX_LOGIN,
    URL_NETFLIX_CONTENT
)

class BeautyfulSoupParser:
    def set_beautyfulsoup(self, html):
        parser = "html.parser"
        self._soup = BeautifulSoup(html, parser)

    def soup_element(self, tag, classname=None, attrs=None):
        result = None
        if classname is not None and attrs is not None:
            result = self._soup.find(tag, class_=classname, attrs=attrs)
        elif classname is not None:
            result = self._soup.find(tag, class_=classname)
        elif attrs is not None:
            result = self._soup.find(tag, attrs=attrs)    
        return result
    
    def soup_elements(self, tag, classname=None, attrs=None):
        result = []
        if classname is not None and attrs is not None:
            result = self._soup.find_all(tag, class_=classname, attrs=attrs)
        elif classname is not None:
            result = self._soup.find_all(tag, class_=classname)
        elif attrs is not None:
            result = self._soup.find_all(tag, attrs=attrs)
        return result

    def soup_close(self):
        self._soup.decompose()


class SeleniumParser:
    def set_selenium(self, url, driver="chrome"):
        options = Options()
        options.add_experimental_option("detach", True)
        # navigator.webdriver = false 로 만들어주는 옵션.
        # options.add_argument("--disable-blink-features=AutomationControlled")
        if driver == "chrome":
            try:
                self._selenium = webdriver.Chrome(options=options)
                self._selenium.get(url)
                self.wait(2)
                return True
            except Exception as e:
                print(str(e))
                return False
        else:
            print("Not supported driver")
            return False
    
    def selenium_element(self, type=None, value=None, target=None):
        result = None
        if type not in ["class", "name", "id", "tag"]:
            print("Not supported type")
            return result
        try:
            if target is None:
                target = self._selenium
            if type == "class":
                result = target.find_element(by=By.CLASS_NAME, value=value)
            elif type == "name":
                result = target.find_element(by=By.NAME, value=value)
            elif type == "id":
                result = target.find_element(by=By.ID, value=value)
            elif type == "tag":
                result = target.find_element(by=By.TAG_NAME, value=value)
            else:
                print("Not supported type")
        except Exception as e:
            print(str(e))
        return result
        
    def selenium_elements(self, type=None, value=None, target=None):
        result = None
        try:
            if target == None:
                target = self._selenium
            if type == "class":
                result = target.find_elements(by=By.CLASS_NAME, value=value)
            elif type == "name":
                result = target.find_elements(by=By.NAME, value=value)
            elif type == "id":
                result = target.find_elements(by=By.ID, value=value)
            elif type == "tag":
                result = target.find_elements(by=By.TAG_NAME, value=value)
            else:
                print("Not supported type")
        except Exception as e:
            print(str(e))
        return result

    def selenium_attribute(self, target, attr):
        result = None
        if attr is not None:
            try:
                result = target.get_attribute(attr)
            except Exception as e:
                print(str(e))
        return result
    
    def selenium_click(self, target):
        if target is not None:
            try:
                target.click()
                self.selenium_wait(2)
                return True
            except Exception as e:
                print(str(e))
                return False
        else:
            print("Target is None")
            return False
    
    def selenium_wait(self, sec):
        sleep(sec)

    def selenium_scroll_move(self, target):
        target.location_once_scrolled_into_view

    def selenium_scroll_down(self):
        if self._selenium is not None:
            try:
                # PAGE_DOWN 키를 이용하여 스크롤 다운
                body = self.selenium_element(type="tag", value="body")
                body.send_keys(Keys.PAGE_DOWN)
                # 웨이팅 (2s)
                self.selenium_wait(2)
                return True
            except Exception as e:
                print(str(e))
                return False
        else:
            return False

    def selenium_scroll_up(self):
        if self._selenium is not None:
            try:
                # PAGE_DOWN 키를 이용하여 스크롤 다운
                body = self.selenium_element(type="tag", value="body")
                body.send_keys(Keys.PAGE_UP)
                # 웨이팅 (2s)
                self.selenium_wait(2)
                return True
            except Exception as e:
                print(str(e))
                return False
        else:
            return False

    def selenium_close(self):
        self._selenium.quit()


class NetflixParser(BeautyfulSoupParser, SeleniumParser):
    def __init__(self):
        self._soup = None
        self._selenium = None

    def login_netflix(self, id, pw):
        try:
            netflix_id = self.selenium_element(type="name", value="userLoginId")
            netflix_pw = self.selenium_element(type="name", value="password")
            netflix_id.send_keys(id)
            netflix_pw.send_keys(pw)
            netflix_pw.send_keys(Keys.RETURN)
            # 로그인 후 페이지 전환 대기 (3s)
            self.selenium_wait(3)
            return True
        except Exception as e:
            print(str(e))
            return False

    def get_content_netflix(self, id):
        url = URL_NETFLIX_CONTENT + "/" + id
        with urlopen(url) as response:
            html = response.read()
        # BeautySoup을 이용하여 데이터 파싱
        if html:
            content = self.parse_content_netflix(html)
            return content
        else:
            return None
            
    def get_most_watched(self):

        self.set_selenium(URL_NETFLIX_LOGIN)
        self.selenium_wait(2)
        self.login_netflix(getattr(settings, "NETFLIX_ID"), getattr(settings, "NETFLIX_PW"))
        self.selenium_wait(2)

        # 시리즈 TOP10과 영화 TOP10을 담을 리스트 초기화
        contents = []

        # 컨텐츠 파싱작업
        content_rows = self.selenium_elements(type="class", value="lolomoRow")
        for content_row in content_rows:
            # 컨텐츠가 화면에 보이도록 스크롤 이동
            self.selenium_scroll_move(target=content_row)
            self.selenium_wait(2)
            # 가져온 컨텐츠가 mostWatched 이면 데이터 파싱 진행
            if self.selenium_attribute(target=content_row, attr="data-list-context") == "mostWatched":
                # 컨텐츠의 더보기 요소를 클릭하여 추가 요소가 렌더링 되도록 함
                handleNext = self.selenium_element(type="class", value="handleNext", target=content_row)
                self.selenium_click(target=handleNext)
                self.selenium_wait(2)
                # 컨텐츠 타이틀
                content_row_title = self.selenium_element(type="class", value="rowHeader", target=content_row).text
                # content_row 에 담긴 데이터 리스트
                content_row_items = self.selenium_elements(type="class", value="slider-item", target=content_row)
                # 컨텐츠별 프리픽스 설정
                type = ""
                if content_row_title == "오늘 대한민국의 TOP 10 시리즈":
                    type = "11"
                elif content_row_title == "오늘 대한민국의 TOP 10 영화":
                    type = "10"
                # 컨텐츠 갯수만큼 반복
                for item in content_row_items:
                    # 필수 정보 파싱
                    rank = self.selenium_element(type="tag", value="svg", target=item)
                    rank = self.selenium_attribute(target=rank, attr="id").split("-")[1]
                    rank = int(rank)
                    link = self.selenium_element(type="tag", value="a", target=item)
                    link = self.selenium_attribute(target=link, attr="href")
                    platform_id = link.split("?")[0].split("/watch/")[1]
                    thumbnail = self.selenium_element(type="tag", value="img", target=item)
                    thumbnail = self.selenium_attribute(target=thumbnail, attr="src")
                    
                    new_content = self.get_content_netflix(platform_id)
                    new_content['rank'] = rank
                    new_content['thumbnails'].append({"type": "10", "thumbnail": thumbnail, "extension": "", "size": 0})

                    # 중복데이터 방지
                    if new_content not in contents:
                            contents.append(new_content)
            # 가져온 컨텐츠가 mostWatched가 아니면 continue
            else:
                continue

        # rank 순으로 정렬
        contents = sorted(contents, key=lambda k: (k['type'], k['rank']))

        # selenium 종료
        self.selenium_close()
        # 파싱한 데이터 리스트 형태로 리턴
        return contents
    
    def parse_content_netflix(self, html):
        self.set_beautyfulsoup(html)        
        schema = self.soup_element(tag="script", attrs={"type": "application/ld+json"})
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
        genres = self.soup_elements(tag="a", classname="item-genres")
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
        self._soup = self.soup_element(tag="div", classname="hero-container")
        # release 추출
        content['release'] = self.soup_element(tag="span", classname="item-year")
        if content['release'] is not None:
            content['release'] = content['release'].text.strip()
        # 상영시간 추출
        content['runtime'] = self.soup_element(tag="span", classname="item-runtime", attrs={"data-uia": "item-runtime"})
        if content['runtime'] is not None:
            content['runtime'] = content['runtime'].text.strip()
        
        self.soup_close()
        print(content)
        return content
    
    def close(self):
        if self._soup is not None:
            self.soup_close()
        if self._selenium is not None:
            self.selenium_close()