from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.Registrate, name='signup'),
    path('check_verify_code/', views.check_verify_code, name='check_verify_code'),
     path('check_verify_code/<str:hash>/<int:user_id>', views.check_verify_code, name='check_verify_code'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
]