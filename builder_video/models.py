from django.db import models


# Create your models here.
class Video(models.Model):
    type = models.CharField(max_length=2, null=False) # 타입 : 10 = movie, 11 = series
    title = models.CharField(max_length=100, null=False) # 타이틀
    synopsis = models.TextField(null=True) # 시놉시스
    release = models.CharField(max_length=20, null=True) # 개봉년도
    runtime = models.CharField(max_length=20, null=True) # 상영시간
    notice_age = models.CharField(max_length=20, null=True) # 연령고지
    grade = models.FloatField(default=0.0) # 평점
    like_count = models.IntegerField(default=0) # 좋아요 수
    view_count = models.IntegerField(default=0) # 조회수
    platform_code = models.CharField(max_length=4, null=False) # 플랫폼 코드 : 1000 = netflix, 1001 = disney+, 1002 = tving, 1003 = waave, 1004 = coupang play, 1005 = watcha, 5000 = Theater
    platform_id = models.CharField(max_length=50, null=False) # 플랫폼별 ID
    is_confirm = models.BooleanField(default=False) # 확인여부
    is_delete = models.BooleanField(default=False) # 삭제여부
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "content_video"


class Actor(models.Model):
    video = models.ManyToManyField(Video, through='VideoActor', related_name="actor") # 출연진
    name = models.CharField(max_length=100, null=False) # 이름
    picture = models.CharField(max_length=100, null=True) # 프로필 이미지
    profile = models.TextField(null=True) # 프로필
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "content_actor"


class Staff(models.Model):
    video = models.ManyToManyField(Video, through='VideoStaff', related_name="staff") # 스태프
    name = models.CharField(max_length=100, null=False) # 이름
    picture = models.CharField(max_length=100, null=True) # 프로필 이미지
    profile = models.TextField(null=True) # 프로필
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "content_staff"


class Genre(models.Model):
    video = models.ManyToManyField(Video, through='VideoGenre', related_name="genre") # 장르
    name = models.CharField(max_length=50, null=False) # 장르
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "content_genre"


class VideoActor(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE) # 비디오 ID
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE) # 출연진
    type = models.CharField(max_length=2, null=False) # 타입 : 10 = main actor, 11 = sub actor
    role = models.CharField(max_length=100, null=True) # 역할
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.actor
    
    class Meta:
        db_table = "content_video_actor"


class VideoStaff(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE) # 비디오 ID
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE) # 스태프
    type = models.CharField(max_length=2, null=False) # 타입 : 10 = director, 11 = creator
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.staff
    
    class Meta:
        db_table = "content_video_staff"


class VideoGenre(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE) # 비디오 ID
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE) # 장르
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.genre
    
    class Meta:
        db_table = "content_video_genre"


class VideoThumbnail(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="thumbnail") # 비디오 ID
    type = models.CharField(max_length=2, null=False) # 타입 : 10 = poster, 11 = thumbnail
    url = models.CharField(max_length=1000, null=False) # 썸네일
    extension = models.CharField(max_length=10, null=False) # 확장자
    size = models.BigIntegerField(null=True) # 사이즈
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.url
    
    class Meta:
        db_table = "content_video_thumbnail"


class VideoWatch(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="watch") # 비디오 ID
    type = models.CharField(max_length=2, null=False) # 타입 : 10 = main contents, 11 = trailer
    url = models.CharField(max_length=100, null=False) # 시청방법
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.url
    
    class Meta:
        db_table = "content_video_watch"


class VideoTag(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="tag") # 비디오 ID
    name = models.CharField(max_length=50, null=False) # 키워드
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "content_video_keyword"


# video_rating
# video_like_log
# video_view_log
# video_review