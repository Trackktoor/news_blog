from django.shortcuts import render
from .models import IP, Post

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

    context = {
        'post': post
    }

    return render(request, 'news/post_view.html', context=context)

