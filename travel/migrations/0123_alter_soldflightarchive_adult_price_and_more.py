# Generated by Django 5.1.7 on 2025-05-30 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0122_soldflightarchive_adult_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldflightarchive',
            name='adult_price',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='soldflightarchive',
            name='baby_price',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='soldflightarchive',
            name='child_price',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
