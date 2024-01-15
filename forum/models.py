from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=100)


class Subject(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='subjects')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class ForumPost(models.Model):
    content = HTMLField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.content
