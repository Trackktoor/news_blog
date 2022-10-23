from django.db import models
from django.contrib.auth.models import AbstractUser
from achievements.models import Achievement

class CustomUser(AbstractUser):
    e_mail = models.EmailField()
    achievements = models.ManyToManyField(Achievement,null=True, blank=True)
    photo = models.ImageField(upload_to=f'', null=True, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.photo.field.upload_to  = f'users_photo/{self.id}/'
        super(CustomUser, self).save(*args, **kwargs)
