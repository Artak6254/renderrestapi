# Generated by Django 5.1.7 on 2025-05-13 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0069_rename_airport_name_flights_filght_airport_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flightdirection',
            old_name='filght_airport_name',
            new_name='flight_airport_name',
        ),
        migrations.RenameField(
            model_name='flights',
            old_name='filght_airport_name',
            new_name='flight_airport_name',
        ),
    ]
