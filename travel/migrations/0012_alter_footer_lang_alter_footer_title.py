# Generated by Django 5.1.7 on 2025-03-24 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0011_delete_languagelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footer',
            name='lang',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='footer',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
