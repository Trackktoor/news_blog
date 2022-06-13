from django.db import models


class IP(models.Model):
    ip = models.CharField(max_length=200)

    def __str__(self):
        return self.ip

class Post(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    views = models.ManyToManyField(IP, related_name='post_views', blank=True)

    def total_views(self):
        return self.views.count()
    
    def __sts__(self):
        return self.title
