from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
