# Generated by Django 5.1.4 on 2025-04-01 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0026_rename_from_field_text_homepagebookingsearch_from_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepagebookingsearch',
            old_name='from_field',
            new_name='from_field_text',
        ),
    ]
