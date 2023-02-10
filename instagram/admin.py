from django.contrib import admin
from . import models


@admin.register(models.InstaPkForCopy)
class InstaPKAdmin(admin.ModelAdmin):
    list_display = ['insta_pk', 'status', ]
    ordering = ['status']


@admin.register(models.MyInstaPage)
class MyInstaPageAdmin(admin.ModelAdmin):
    list_display = ['user_key', 'username', 'user_id']
    ordering = ['username']


@admin.register(models.InstaUserForCopy)
class CommentForUseAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_id', ]
    ordering = ['username']
