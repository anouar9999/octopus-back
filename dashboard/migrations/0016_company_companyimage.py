# Generated by Django 5.0.6 on 2024-06-14 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_alter_company_companyname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='CompanyImage',
            field=models.ImageField(null=True, upload_to='companies_images/'),
        ),
    ]
