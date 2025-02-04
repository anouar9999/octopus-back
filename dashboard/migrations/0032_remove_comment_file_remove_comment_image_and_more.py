# Generated by Django 5.0.6 on 2024-07-06 03:24

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_alter_comment_file_alter_comment_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='file',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='image',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
