from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(Article, ArticleAdmin)
