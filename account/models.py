import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    # 타입 : 10 = email, 11 = google, 12 = facebook, 13 = apple, 14 = kakao, 15 = naver
    type = models.CharField(max_length=2, null=False)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=60)
    nickname = models.CharField(max_length=40, unique=True, null=True)
    profile_image = models.CharField(max_length=100, null=True)
    profile = models.TextField(null=True)
    is_agree = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    token = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = "rvvs_user"


class AccessLog(models.Model):
    status = models.IntegerField(null=False)
    path = models.CharField(max_length=200, null=False)
    ip = models.CharField(max_length=50, null=False)
    user_agent = models.CharField(max_length=200, null=False)
    user_id = models.IntegerField(null=True)
    message = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "rvvs_login_log"

