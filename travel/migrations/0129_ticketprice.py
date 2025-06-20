# Generated by Django 5.1.7 on 2025-05-30 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0128_bookingtickets'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_type', models.CharField(choices=[('adult', 'Adult'), ('child', 'Child'), ('baby', 'Baby')], max_length=10)),
                ('price', models.PositiveIntegerField()),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.passengers')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passenger_tickets', to='travel.tickets')),
            ],
        ),
    ]
