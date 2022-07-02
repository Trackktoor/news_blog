from django.shortcuts import render

from users.models import CustomUser
from .models import IP, Post
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
    print(posts)

    context = {
        'posts': posts
    }

    return render(request, 'news/home.html', context)

def post_view(request, id):
    post = Post.objects.get(id=id)

    ip = get_client_ip(request)

    ip_created = IP.objects.get_or_create(ip=ip)
    post.views.add(ip_created[0])

    post.save()

    context = {
        'post': post
    }

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
