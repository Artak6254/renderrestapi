# Generated by Django 5.1.7 on 2025-04-19 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0043_remove_flights_departure_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flights',
            name='arrive_time',
        ),
        migrations.RemoveField(
            model_name='flights',
            name='return_arrive_time',
        ),
        migrations.AddField(
            model_name='flights',
            name='arrival_time',
            field=models.CharField(default='00:00', max_length=20),
        ),
        migrations.AddField(
            model_name='flights',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='flights',
            name='return_arrival_time',
            field=models.CharField(default='00:00', max_length=20),
        ),
        migrations.AlterField(
            model_name='flights',
            name='departure_date',
            field=models.CharField(default='01-01-2025', max_length=20),
        ),
        migrations.AlterField(
            model_name='flights',
            name='departure_time',
            field=models.CharField(default='00:00', max_length=20),
        ),
        migrations.AlterField(
            model_name='flights',
            name='return_date',
            field=models.CharField(default='02-01-2025', max_length=20),
        ),
        migrations.AlterField(
            model_name='flights',
            name='return_departure_time',
            field=models.CharField(default='00:00', max_length=20),
        ),
        migrations.AlterField(
            model_name='flightseats',
            name='seat_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='adult_count',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='baby_count',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='child_count',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='departure_price',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='return_price',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.CreateModel(
            name='Passengers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=60)),
                ('title', models.CharField(max_length=10)),
                ('full_name', models.CharField(max_length=100)),
                ('date_of_birth', models.CharField(max_length=20)),
                ('citizenship', models.CharField(max_length=30)),
                ('passport_serial', models.CharField(max_length=60)),
                ('departure_baggage_weight', models.CharField(max_length=20)),
                ('return_baggage_weight', models.CharField(max_length=20)),
                ('departure_seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_passengers', to='travel.flightseats')),
                ('return_seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_passengers', to='travel.flightseats')),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passengers', to='travel.tickets')),
            ],
        ),
        migrations.DeleteModel(
            name='Passngers',
        ),
    ]
