# Generated by Django 5.1.7 on 2025-05-30 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0121_tickets_adult_price_tickets_child_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldflightarchive',
            name='adult_price',
            field=models.CharField(default='20000', max_length=50),
        ),
        migrations.AddField(
            model_name='soldflightarchive',
            name='child_price',
            field=models.CharField(default='20000', max_length=50),
        ),
    ]
