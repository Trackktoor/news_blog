from django.db import models
from users.models import CustomUser

class IP(models.Model):
    ip = models.CharField(max_length=200)

    def __str__(self):
        return self.ip

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.id
    
    

class Post(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    views = models.ManyToManyField(IP, related_name='post_views', blank=True)
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(Like)

    def total_views(self):
        return self.views.count()

    def __str__(self):
        return self.title

    def add_like(self, user_id):
        user = CustomUser.objects.get(id=user_id)
        
        like = Like(
            user = user,
        ).save()

        like = Like.objects.filter(user=user).order_by('-id')[0]

        self.likes.add(like)

        self.save()
    
    def sum_likes(self, user_id):

        user = CustomUser.objects.get(id=user_id)

        like = Like.objects.filter(user=user).order_by('-id')[0]

        return like.id
        

        