from django.db import models
from django.urls import  reverse
# Create your models here.
from  datetime import datetime
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    content = models.TextField()
    user = User

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

