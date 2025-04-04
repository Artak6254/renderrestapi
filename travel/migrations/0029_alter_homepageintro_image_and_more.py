# Generated by Django 5.1.7 on 2025-04-03 16:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0028_alter_footerlinks_url_alter_footersocial_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepageintro',
            name='image',
            field=models.ImageField(upload_to='travel/static/image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'svg'])]),
        ),
        migrations.AlterField(
            model_name='homepagewhychooseus',
            name='image',
            field=models.ImageField(upload_to='travel/static/image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'svg'])]),
        ),
        migrations.AlterField(
            model_name='logo',
            name='logo',
            field=models.ImageField(upload_to='travel/static/image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'svg'])]),
        ),
    ]
