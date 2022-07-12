from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('<int:id>', views.post_view, name='post_view'),
    path('create_post', views.create_post_view, name='create_post_view'),
    path('delete_post/<int:id>', views.delete_post_view, name='delete_post_view'),
    path('change_post/<int:id>', views.change_post_view, name='change_post_view'),
]
