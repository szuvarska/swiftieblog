# Generated by Django 4.2.7 on 2024-01-21 16:39

from django.db import migrations

from blog.models import UserAccount
from forum.models import Subject, ForumPost


def update_counts(apps, schema_editor):
    UserAccount = apps.get_model('blog', 'UserAccount')

    for user_account in UserAccount.objects.all():
        user_account.subjects_count = Subject.objects.filter(author=user_account.user).count()
        user_account.posts_count = ForumPost.objects.filter(author=user_account.user).count()
        user_account.save()


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0002_alter_forumpost_content'),
    ]

    operations = [
        migrations.RunPython(update_counts),
    ]
