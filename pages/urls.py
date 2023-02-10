from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # path('', views.home_view, name='home_url'),
    path('', views.list_view, name='home_url'),
    path('blog/<int:pk>/', views.detail_view, name='detail_view_url'),
    path('blog/create/', views.AddBlogView.as_view(), name='create_blog_url')
]
