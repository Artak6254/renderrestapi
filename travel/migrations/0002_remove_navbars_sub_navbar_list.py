# Generated by Django 5.1.7 on 2025-03-23 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='navbars',
            name='sub_navbar_list',
        ),
    ]
