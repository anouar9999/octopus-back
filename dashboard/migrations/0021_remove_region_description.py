# Generated by Django 5.0.6 on 2024-07-01 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_rename_name_projectimage_info_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='description',
        ),
    ]
