from django.urls import path
from . import views 

app_name = 'facial_auth' 

urlpatterns = [
    path('register/', views.face_registration, name='register'),
    path('login/', views.face_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('video-feed/', views.video_feed, name='video_feed'),
    path('activate-camera', views.activate_camera, name='activate_camera'),
    path('mouse/', views.mouse_feed, name='mouse_feed'),
    path('mouse_feed/', views.mouse_video_feed, name='mouse_video_feed'),
]

