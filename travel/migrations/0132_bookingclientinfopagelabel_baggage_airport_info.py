# Generated by Django 5.1.7 on 2025-05-31 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0131_rename_adult_price_tickets_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingclientinfopagelabel',
            name='baggage_airport_info',
            field=models.TextField(default='լրացուցիչ տեղեկությունների'),
        ),
    ]
