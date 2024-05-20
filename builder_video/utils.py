import os
from datetime import datetime
from urllib.request import urlretrieve
import uuid
from django.utils.html import escape

def html_escape(text):
    return escape(text)

def make_filename(name):
    # 파일명에서 확장자 추출
    file_ext = name.split(".")[-1]
    # 혹시 파라미터가 붙어있다면 삭제
    file_ext = file_ext.split("?")[0]
    # 소문자로 변환
    file_ext = file_ext.lower()
    # 파일명 반환
    return f"{uuid.uuid4()}.{file_ext}"

def save_file_from_url(file, file_path):
    try:
        urlretrieve(file, file_path)
        return True
    except Exception as e:
        print(e)
        return False
    
def get_file_extension(file_name):
    return file_name.split(".")[-1].lower()

def get_file_size(file):
    if os.path.isfile(file):
        return os.path.getsize(file)
    else:
        return None

def write_log(log_path, message):
    with open(log_path, "a") as file:
        file.write(message + "\n")

def write_db_log(type, message):
    log_path = "data/log/db_{}_{}_{}.log".format(datetime.now().year, datetime.now().month, datetime.now().day)
    log_message = "[{}]".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"))
    log_message += "[{}]".format(type)
    log_message += " - {}\n".format(message)
    with open(log_path, "a") as file:
        file.write(message + "\n")