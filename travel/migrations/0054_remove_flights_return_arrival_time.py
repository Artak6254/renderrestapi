# Generated by Django 5.1.7 on 2025-05-05 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0053_remove_flights_return_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flights',
            name='return_arrival_time',
        ),
    ]
