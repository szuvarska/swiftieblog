# Generated by Django 4.2.7 on 2024-01-21 16:33

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumpost',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
