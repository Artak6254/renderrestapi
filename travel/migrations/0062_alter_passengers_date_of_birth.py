# Generated by Django 5.1.7 on 2025-05-10 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0061_alter_passengers_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passengers',
            name='date_of_birth',
            field=models.DateField(default='2000-01-01', null=True),
        ),
    ]
