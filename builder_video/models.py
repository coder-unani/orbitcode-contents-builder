import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Video(models.Model):
    # 타입 : 10=movie, 11=series
    type = models.CharField(max_length=2, null=False, db_index=True)
    # 타이틀
    title = models.CharField(max_length=100, null=False, db_index=True)
    # 시놉시스
    synopsis = models.TextField(null=True)
    # 개봉년도
    release = models.CharField(max_length=20, null=True)
    # 상영시간
    runtime = models.CharField(max_length=20, null=True)
    # 연령고지
    notice_age = models.CharField(max_length=20, null=True)
    # 평점
    grade = models.FloatField(default=0.0, db_index=True)
    # 좋아요 수
    like_count = models.IntegerField(default=0)
    # 조회수
    view_count = models.IntegerField(default=0)
    # 플랫폼 코드: 10=netflix, 11=disney+, 12=tving, 13=waave, 14=coupang play, 15=watcha, 50=Theater
    platform_code = models.CharField(max_length=2, null=False, db_index=True)
    # 플랫폼별 ID
    platform_id = models.CharField(max_length=50, null=False)
    # 확인여부
    is_confirm = models.BooleanField(default=False)
    # 삭제여부
    is_delete = models.BooleanField(default=False)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "rvvs_video"


class Actor(models.Model):
    video = models.ManyToManyField(Video, through='VideoActor', related_name="actor")
    # 배우이름
    name = models.CharField(max_length=100, null=False, db_index=True)
    # 배우사진
    picture = models.CharField(max_length=200, null=True)
    # 프로필
    profile = models.TextField(null=True)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "rvvs_actor"


class Staff(models.Model):
    video = models.ManyToManyField(Video, through='VideoStaff', related_name="staff")
    # 이름
    name = models.CharField(max_length=100, null=False, db_index=True)
    # 프로필 이미지
    picture = models.CharField(max_length=200, null=True)
    # 프로필
    profile = models.TextField(null=True)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "rvvs_staff"


class Genre(models.Model):
    video = models.ManyToManyField(Video, through='VideoGenre', related_name="genre")
    # 장르
    name = models.CharField(max_length=50, null=False, db_index=True)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "rvvs_genre"


class VideoActor(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # 출연진
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    # 타입 : 10=main actor, 11=sub actor
    type = models.CharField(max_length=2, null=False)
    # 역할
    role = models.CharField(max_length=100, null=True)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.actor
    
    class Meta:
        db_table = "rvvs_video_actor"


class VideoStaff(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # 스태프
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # 타입 : 10=director, 11=creator
    type = models.CharField(max_length=2, null=False)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.staff
    
    class Meta:
        db_table = "rvvs_video_staff"


class VideoGenre(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # 장르
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.genre
    
    class Meta:
        db_table = "rvvs_video_genre"


class VideoThumbnail(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="thumbnail")
    # 타입 : 10=poster, 11=thumbnail
    type = models.CharField(max_length=2, null=False)
    # 썸네일 URL
    url = models.CharField(max_length=1000, null=False)
    # 확장자
    extension = models.CharField(max_length=10, null=False)
    # 사이즈
    size = models.BigIntegerField(null=True)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.url
    
    class Meta:
        db_table = "rvvs_video_thumbnail"


class VideoWatch(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="watch")
    # 타입: 10=main contents, 11=trailer
    type = models.CharField(max_length=2, null=False)
    # 시청 URL
    url = models.CharField(max_length=100, null=False)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.url
    
    class Meta:
        db_table = "rvvs_video_watch"


class VideoTag(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="tag")
    # 태그 이름
    name = models.CharField(max_length=50, null=False, db_index=True)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "rvvs_video_keyword"


class VideoRank(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="rank")
    # 타입 : 10=netflix, 11=disney+, 12=tving, 13=waave, 14=coupang play, 15=watcha, 50=Theater
    platform_code = models.CharField(max_length=2, null=False)
    # 기준 코드
    rank_code = models.CharField(max_length=20, null=False)
    # 랭킹 분류
    rank_type = models.CharField(max_length=2, null=False)
    # 랭킹
    rank = models.IntegerField(default=0)
    # 생성일, 수정일
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.rank

    class Meta:
        db_table = "rvvs_video_rank"


# video_like_log
# video_view_log
