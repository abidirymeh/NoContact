from django.urls import path
from . import views  # Import absolument nécessaire

app_name = 'facial_auth'  # Namespace important

urlpatterns = [
    path('register/', views.face_registration, name='register'),  # Simplifié
    path('login/', views.face_login, name='login'),  # Simplifié
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.custom_logout, name='logout'),
]

