# Generated by Django 5.1.4 on 2025-03-31 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0025_alter_calendarfieldlist_options_alter_footer_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepagebookingsearch',
            old_name='from_field_text',
            new_name='from_field',
        ),
    ]
