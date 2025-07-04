# Generated by Django 5.1.7 on 2025-05-27 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0107_delete_baggagepolicy_delete_charge_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlightSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_here', models.CharField(max_length=120)),
                ('to_there', models.CharField(max_length=120)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('time', models.TimeField()),
                ('flight_type', models.CharField(choices=[('departure', 'Departure'), ('return', 'Return')], max_length=10)),
                ('flight_airport_name', models.CharField(max_length=100)),
                ('flight_airport_short_name', models.CharField(max_length=100)),
                ('arrival_airport_name', models.CharField(max_length=100)),
                ('arrival_airport_short_name', models.CharField(max_length=100)),
                ('bort_number', models.CharField(default='Unknown', max_length=50)),
            ],
        ),
    ]
