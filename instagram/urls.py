from django.urls import path
from . import views


urlpatterns = [
    path('add-user/', views.add_user_view, name='add_user_url'),
    path('add-pk/<int:userid>/', views.add_pk_view, name='add_pk_url'),
    path('user-list/', views.user_list_view, name='user_list_url'),
    path('posting/<str:password>/<str:user_pub>/', views.posting_view, name='posting_url'),
    path('get-settings/<str:user_pub>/', views.get_settings, name='get_settings_url'),
    path('user-pub-list/', views.user_pub_list_view, name='user_pub_list_url')
]
