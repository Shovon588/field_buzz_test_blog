from django.contrib import admin
from . models import Blog, ReaderInfo, Comment

# Register your models here.
admin.site.register(Blog)
admin.site.register(ReaderInfo)
admin.site.register(Comment)
