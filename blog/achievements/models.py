from django.db import models

class Achievement(models.Model):
    name = models.CharField(max_length=255)
    conditions = models.TextField()

    def __str__(self):
        return self.name