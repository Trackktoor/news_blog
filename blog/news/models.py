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
        
        for like in self.likes.through.objects.all():
            if Like.objects.get(id=like.like_id).user_id  == user_id:
                print('d')
                print(like.like_id)
                like.delete()
                Like.objects.get(id=like.like_id).delete()
                break
        else:
            like = Like(
                user = user,
            ).save()

            like = Like.objects.filter(user=user).order_by('-id')[0]

            self.likes.add(like)
            self.save()
            
        
    
    def sum_likes(self, post_id):

        sum_likes = Post.likes.through.objects.all().filter(post_id=post_id).count()
        
        return sum_likes

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Пользователь: ' + self.user.username 
        

        