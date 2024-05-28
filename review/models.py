from django.db import models
from django.utils import timezone


# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=True)
    rating = models.FloatField(default=0.0)
    like_count = models.IntegerField(default=0)
    is_spoiler = models.BooleanField(default=False)
    is_expect = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    user_id = models.IntegerField(null=False)
    user_profile_image = models.CharField(max_length=100, null=True)
    user_nickname = models.CharField(max_length=40, null=False)
    video_id = models.IntegerField(null=False, db_index=True)
    video_title = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "rvvs_review"
        ordering = ['-created_at']

