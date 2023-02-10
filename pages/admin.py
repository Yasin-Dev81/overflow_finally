from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class DatabaseNameAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'is_active',
        'datetime_modified'
    ]
    list_filter = ['datetime_modified']
    ordering = ['datetime_modified']
