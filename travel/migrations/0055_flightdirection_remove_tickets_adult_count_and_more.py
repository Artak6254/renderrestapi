# Generated by Django 5.1.7 on 2025-05-07 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0054_remove_flights_return_arrival_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlightDirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_there', models.CharField(max_length=100)),
                ('to_there', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='tickets',
            name='adult_count',
        ),
        migrations.RemoveField(
            model_name='tickets',
            name='baby_count',
        ),
        migrations.RemoveField(
            model_name='tickets',
            name='child_count',
        ),
        migrations.RemoveField(
            model_name='tickets',
            name='departure_price',
        ),
        migrations.RemoveField(
            model_name='tickets',
            name='return_price',
        ),
        migrations.AddField(
            model_name='tickets',
            name='price',
            field=models.CharField(default='0', max_length=10),
        ),
        migrations.AddField(
            model_name='tickets',
            name='ticket_number',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.CreateModel(
            name='PassangersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_count', models.IntegerField(default=0)),
                ('child_count', models.IntegerField(default=0)),
                ('baby_count', models.IntegerField(default=0)),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passangers_count', to='travel.flights')),
            ],
        ),
    ]
