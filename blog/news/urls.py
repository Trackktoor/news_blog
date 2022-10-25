from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view.as_view(), name='home_view'),
    path('paginate/<int:page_paginator>', views.home_view.as_view(), name='home_view__paginate'),
    path('<int:id>', views.post_view.as_view(), name='post_view'),
    path('create_post', views.create_post_view.as_view(), name='create_post_view'),
    path(
        'delete_post/<int:id>',
        views.delete_post_view.as_view(),
        name='delete_post_view'
    ),
    path(
        'change_post/<int:id>',
        views.change_post_view.as_view(),
        name='change_post_view'
    ),
    path(
        'add_like_post/<int:id>/<int:user_id>',
        views.add_like_post_view.as_view(),
        name='add_like_post'
    ),
    path('add_comment/<int:id>', views.comment_add_view.as_view(), name='add_comment'),
    path('my_posts/<int:id>', views.User_posts.as_view(), name='User_posts'),
    path('top_raiting', views.Top_rating.as_view(), name='Top_raiting')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
