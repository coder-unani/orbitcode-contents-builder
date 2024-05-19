from django.db import models

# Create your models here.
class Video(models.Model):
    kind = models.CharField(max_length=2, null=False) # 타입 : 10 = movie, 11 = series
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
        db_table = "content_videos"

class Actor(models.Model):
    kind = models.CharField(max_length=2, null=False) # 타입 : 10 = 주연, 11 = 조연
    name = models.CharField(max_length=100, null=False) # 이름
    picture = models.CharField(max_length=100, null=True) # 프로필 이미지
    profile = models.TextField(null=True) # 프로필
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "content_actors"

class Staff(models.Model):
    kind = models.CharField(max_length=2, null=False) # 타입 : 10 = director, 11 = writer, 12 = producer
    name = models.CharField(max_length=100, null=False) # 이름
    picture = models.CharField(max_length=100, null=True) # 프로필 이미지
    profile = models.TextField(null=True) # 프로필
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "content_staffs"

class Genre(models.Model):
    name = models.CharField(max_length=50, null=False) # 장르
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "content_genres"

class VideoActor(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="casts") # 비디오 ID
    cast = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="video_cast") # 출연진
    picture = models.CharField(max_length=100, null=True) # 출연진 사진
    role = models.CharField(max_length=100, null=False) # 역할
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.cast
    
    class Meta:
        db_table = "content_video_actors"

class VideoStaff(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="staffs") # 비디오 ID
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="video_staff") # 스태프
    role = models.CharField(max_length=100, null=False) # 역할
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.staff
    
    class Meta:
        db_table = "content_video_staffs"


class VideoGenre(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="genres") # 비디오 ID
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="video_genre") # 장르
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.genre
    
    class Meta:
        db_table = "content_video_genres"

class VideoThumbnail(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="thumbnails") # 비디오 ID
    kind = models.CharField(max_length=2, null=False) # 타입 : 10 = poster, 11 = thumbnail
    thumbnail = models.CharField(max_length=200, null=False) # 썸네일
    extension = models.CharField(max_length=10, null=False) # 확장자
    size = models.BigIntegerField(null=True) # 사이즈
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.thumbnail
    
    class Meta:
        db_table = "content_video_thumbnails"

class VideoWatch(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="watchs") # 비디오 ID
    kind = models.CharField(max_length=2, null=False) # 타입 : 10 = main contents, 11 = trailer
    url = models.CharField(max_length=100, null=False) # 시청방법
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.watch
    
    class Meta:
        db_table = "content_video_watchs"

class VideoKeyword(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="keywords") # 비디오 ID
    keyword = models.CharField(max_length=50, null=False) # 키워드
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    def __str__(self):
        return self.keyword
    
    class Meta:
        db_table = "content_video_keywords"


# video_rating
# video_like_log
# video_view_log
# video_review