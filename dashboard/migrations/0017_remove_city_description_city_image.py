# Generated by Django 5.0.6 on 2024-06-21 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_company_companyimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='description',
        ),
        migrations.AddField(
            model_name='city',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='city_images/'),
        ),
    ]
