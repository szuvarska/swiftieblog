from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=31)
    pub_date = models.DateTimeField()


class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
