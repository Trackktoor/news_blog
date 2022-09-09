from multiprocessing import context
from django.shortcuts import render, redirect

from users.models import CustomUser
from .models import IP, Post, Comment
from .forms import *

def get_client_ip(request):
    x_forwared_for = request.META.get('HTTP_X_FORWARED_FOR')
    if x_forwared_for:
        ip = x_forwared_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home_view(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'news/home.html', context)

def post_view(request, id, context_dict = {}):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post_comment_id = id) or []
    ip = get_client_ip(request)

    ip_created = IP.objects.get_or_create(ip=ip)
    post.views.add(ip_created[0])
    post.save()

    context = {
        'post': post,
        'sum_likes': post.sum_likes(id),
        'comments': comments,
    }

    context = context_dict | context

    return render(request, 'news/post_view.html', context=context)

def create_post_view(request):
    if request.method == 'GET':
        form = CreatePostForm()
    elif request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():

            post = Post(
                title=form.cleaned_data['title'], 
                content = form.cleaned_data['content'],
                CustomUser = CustomUser.objects.get(id=request.user.id)
                )
            
            post.save()

            context = {
                'post': post
            }

            return render(request, 'news/post_view.html', context)
    
    context = {
        'form': form
        }
    return render(request, 'news/create_post.html', context)

def delete_post_view(request, id):
    post = Post.objects.get(id=id)
    if request.user.id == post.CustomUser.id:
        post.delete()
        return render(request, 'news/home.html')
    else:
        return render(request, 'news/home.html')

def change_post_view(request, id):
    post = Post.objects.get(id=id)
    if request.user.id == post.CustomUser.id:
        if request.method == 'POST':
            post.title = request.POST.get('title')
            post.content = request.POST.get('content')
            post.save()
            return redirect(f'/{post.id}')
        else:
            form = ChangePostForm()
            context = {
                'form': form,
                'post': post
            }
            return render(request, 'news/change_post.html', context)
    else:
        return render(request, 'news/home.html')

def add_like_post_view(request, id, user_id):
    post = Post.objects.get(id=id)
    post.add_like(user_id)

    return post_view(request, id)

def comment_add_view(request, id):
    form = CommentPostForm(request.POST or None)
    if form.is_valid():
        comment_body = form.cleaned_data.get('comment_body')
        comment = Comment(user=CustomUser.objects.get(id=request.user.id),body=comment_body, post_comment = Post.objects.get(id=id))
        comment.save()

        return post_view(request, id)
    else:
        return post_view(request, id, context_dict={'error_validate': 'Вы не написали комментарий!'})
