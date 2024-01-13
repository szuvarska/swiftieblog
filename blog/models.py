from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='article_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=31)
    pub_date = models.DateTimeField()


class Category(models.Model):
    name = models.CharField(max_length=100)


class Subject(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='subjects')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class ForumPost(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.content


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
