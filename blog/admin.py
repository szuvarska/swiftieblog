from django.contrib import admin

from .models import Article, ForumPost, Category, Subject

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(ForumPost)
