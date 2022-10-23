from django.shortcuts import render, redirect
from users.models import CustomUser
from .models import IP, Post, Comment
from .forms import *
from django.views import View
from .utils import get_client_ip, VerificationUserMixin
from achievements.util import first_post_achievement


class home_view(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'news/home.html', context = {'posts': posts})


class post_view(View):
    def get(self, request, id, context_dict = {}):
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

class create_post_view(VerificationUserMixin):

    def get(self, request):
        form = CreatePostForm()
        context = {
            'form': form
            }
        return render(request, 'news/create_post.html', context)

    def post(self, request):
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

            first_post_achievement(request.user.id)

            return render(request, 'news/post_view.html', context)


class delete_post_view(VerificationUserMixin):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        if request.user.id == post.CustomUser.id:
            post.delete()
            return redirect('/')
        else:
            return redirect('/')


class change_post_view(VerificationUserMixin):
    def post(self, request, id):
        post = Post.objects.get(id=id)

        if request.user.id == post.CustomUser.id:
            
            post.title = request.POST.get('title')
            post.content = request.POST.get('content')
            post.save()
            return redirect(f'/{post.id}')

    def get(self, request, id):
        post = Post.objects.get(id=id)

        form = ChangePostForm()
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'news/change_post.html', context=context)


class add_like_post_view(VerificationUserMixin):
    def post(self, request, id, user_id):
        post = Post.objects.get(id=id)
        post.add_like(user_id)

        return post_view(request, id)

    def get(self, request, id, user_id):
        post = Post.objects.get(id=id)
        post.add_like(user_id)

        return post_view().get(id=id, request=request)


class comment_add_view(VerificationUserMixin):
    def post(self, request, id):
        form = CommentPostForm(request.POST or None) 
        if form.is_valid():
            comment_body = form.cleaned_data.get('comment_body')
            comment = Comment(user=CustomUser.objects.get(id=request.user.id),body=comment_body, post_comment = Post.objects.get(id=id))
            comment.save()

            return post_view().get(request, id)
        else:
            return post_view().get(request=request, id=id, context_dict={'error_validate': 'Вы не написали комментарий!'})

            
class User_posts(VerificationUserMixin):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        posts = Post.objects.filter(CustomUser=id)

        return render(request, 'news/user_posts.html', {'posts': posts})

class Top_rating(View):
    def get(self, request):
        posts = Post.objects.order_by('likes')

        return render(request, 'news/top_raiting.html', {'posts': posts})
