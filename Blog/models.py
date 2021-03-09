from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    slug = AutoSlugField(populate_from="title", blank=True, unique_with=["title"])
    post = models.TextField()
    published = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s by %s" % (self.title, self.user.username)


class ReaderInfo(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='readerinfos')
    read_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s at %s" % (self.post.title, self.read_time)


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=55, blank=True)
    comment = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s at %s" % (self.comment, self.post.title)
