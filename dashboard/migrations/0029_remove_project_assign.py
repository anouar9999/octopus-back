# Generated by Django 5.0.6 on 2024-07-04 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_remove_project_lang_remove_project_lat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='assign',
        ),
    ]
