# Generated by Django 5.1.7 on 2025-04-19 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0041_remove_passngerlist_raw_passport_serial_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_here', models.CharField(max_length=120)),
                ('to_there', models.CharField(max_length=120)),
                ('airport_name', models.CharField(default='Unknown Airport', max_length=100)),
                ('airport_short_name', models.CharField(default='Unknown short Airport', max_length=100)),
                ('departure_date', models.CharField(max_length=50)),
                ('departure_time', models.CharField(max_length=50)),
                ('arrive_time', models.CharField(max_length=50)),
                ('return_date', models.CharField(max_length=50)),
                ('return_departure_time', models.CharField(max_length=50)),
                ('return_arrive_time', models.CharField(max_length=50)),
                ('bort_number', models.CharField(max_length=50)),
                ('departure_price', models.CharField(max_length=50)),
                ('return_price', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FlightSeats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=20)),
                ('is_taken', models.BooleanField(default=False)),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight_seats', to='travel.flights')),
            ],
        ),
        migrations.CreateModel(
            name='Passngers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=60)),
                ('title', models.CharField(max_length=60)),
                ('full_name', models.CharField(max_length=60)),
                ('date_of_birth', models.CharField(max_length=50)),
                ('citizenship', models.CharField(max_length=20)),
                ('passport_serial', models.CharField(max_length=60)),
                ('departure_baggage_weight', models.CharField(max_length=60)),
                ('return_baggage_weight', models.CharField(max_length=60)),
                ('departure_seat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_seat', to='travel.flightseats')),
                ('return_seat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_seat', to='travel.flightseats')),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('is_sold', models.BooleanField(default=False)),
                ('adult_count', models.CharField(max_length=50)),
                ('child_count', models.CharField(max_length=50)),
                ('baby_count', models.CharField(max_length=50)),
                ('departure_price', models.CharField(max_length=20)),
                ('return_price', models.CharField(max_length=20)),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='travel.flights')),
            ],
        ),
        migrations.DeleteModel(
            name='AvailableTickets',
        ),
        migrations.RemoveField(
            model_name='passngerlist',
            name='ticket_id',
        ),
        migrations.DeleteModel(
            name='PlaneSeats',
        ),
        migrations.AddField(
            model_name='passngers',
            name='ticket_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passangers', to='travel.tickets'),
        ),
        migrations.DeleteModel(
            name='PassngerList',
        ),
        migrations.DeleteModel(
            name='SoldTickets',
        ),
    ]
