## git repository 초기화
git init

## 기본 브랜치를 master에서 main으로 옴김
git branch -M main 

## Python 가상환경 셋팅
python3 -m venv .venv

## 파이썬 가상환경 실행
source .venv/bin/activate

## 가상환경 셋팅 확인
which python3
/Users/unani/developments/projects/orbitcode/contents-builder/.venv/bin/python3

## django 설치
pip install django

## 의존성 설치
pip install django-environ
pip install selenium
pip install beautifulsoup4
pip install boto3
pip install uuid
pip install mysqlclient

## requirements.txt 작성
pip freeze > requirements.txt

## django project 생성
django-admin startproject config .

## .env 환경변수 파일 생성
touch .env.development
touch .env.production

# templates 디렉토리 생성
mkdir templates

# static 디렉토리 생성
mkdir static

## 개발환경 변수 설정
vi .env.development
DEBUG
SECRET_KEY
LANGUAGE_CODE
TIME_ZONE
DB_HOST
DB_PORT
DB_NAME
DB_USER_NAME
DB_USER_PASSWORD

## django 기본 환경설정
cd config
mkdir settings
mv settings.py settings/

/manage.py
config.settings => config.settings.settings 변경

/config/asgi.py
config.settings => config.settings.settings 변경

/config/wsgi.py
config.settings => config.settings.settings 변경

/config/settings/settings.py
# BASE_DIR 변경
BASE_DIR = Path(__file__).resolve().parent.parent.parent 

# ENV 환경변수 설정
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(
    env_file = os.path.join(BASE_DIR, '.env.development')
)

# env를 사용하도록 변경
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
LANGUAGE_CODE = env('LANGUAGE_CODE')
TIME_ZONE = env('TIME_ZONE')

# allow hosts 추가
ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
]

# DB 설정 변경
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER_NAME'),
        'PASSWORD': env('DB_USER_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# TEMPLATES 경로 변경
# TEMPLATES > DIRS >
os.path.join(BASE_DIR, 'templates'),

# STATIC 경로 변경
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

## django app 생성
django-admin startapp account
django-admin startapp builder-video

## settings.py 에 앱 추가
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'account',
    'builder_video',
]

## django database migration
python3 manage.py makemigrations
python3 manage.py migrate

## django superuser 생성
python3 manage.py createsuperuser --username=orbitcode --email=groot@orbitcode.kr

## django project 시작
python3 manage.py runserver 0.0.0.0:8000

## 이 후 개발 과정은 github에서 확인