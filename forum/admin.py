from django.contrib import admin

from .models import Category, Subject, ForumPost

admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(ForumPost)