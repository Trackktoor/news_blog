from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('<int:id>', views.post_view, name='post_view'),
    path('create_post', views.create_post_view, name='create_post_view'),
]
