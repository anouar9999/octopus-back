# Generated by Django 5.0.6 on 2024-07-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_projectimagecomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectimagecomment',
            name='user',
        ),
        migrations.AddField(
            model_name='projectimagecomment',
            name='user_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
