# Generated by Django 5.1.7 on 2025-04-05 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0030_alter_homepageintro_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bort_number', models.CharField(max_length=100)),
                ('from_here', models.CharField(max_length=120)),
                ('to_there', models.CharField(max_length=120)),
                ('adult_count', models.CharField(max_length=50)),
                ('child_count', models.CharField(max_length=50)),
                ('baby_count', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='BookingFlights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_date', models.CharField(max_length=150)),
                ('checkout_date', models.CharField(max_length=150)),
                ('checkin_time', models.CharField(max_length=150)),
                ('checkout_time', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight_details', to='travel.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_flights',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='travel.bookingflights'),
        ),
        migrations.CreateModel(
            name='BookingPassengers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=60)),
                ('departure_baggage_weight', models.CharField(max_length=80)),
                ('return_baggage_weight', models.CharField(max_length=60)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passengers', to='travel.booking')),
            ],
        ),
    ]
