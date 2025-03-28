from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView  # Ajoutez cet import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/')),  # Redirection vers /login/
    path('', include(('facial_auth.urls', 'facial_auth'), namespace='facial_auth')),
    path('logout/', LogoutView.as_view(), name='logout'),

]

