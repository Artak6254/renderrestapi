# Generated by Django 5.1.7 on 2025-05-18 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0087_onlineregistrationpage_conditions_page_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topheadingonlinereg',
            name='page2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='air40', to='travel.onlineregistrationpage'),
        ),
    ]
