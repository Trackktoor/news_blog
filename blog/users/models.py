from django.db import models
from django.contrib.auth.models import AbstractUser
from achievements.models import Achievement

class CustomUser(AbstractUser):
    e_mail = models.EmailField()
    achievements = models.ManyToManyField(Achievement)

    def __str__(self):
        return self.username
