# Generated by Django 5.1.7 on 2025-03-31 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0024_footer_owner_homepagebookingsearch_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendarfieldlist',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='footer',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='footerlinks',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='footersocial',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='homepagebookingsearch',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='homepagefaq',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='homepageintro',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='homepagequestion',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='homepagewhychooseus',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='logo',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='navbars',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='passangerfieldlist',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='reasonslist',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='subnavbarslist',
            options={'ordering': ['id']},
        ),
    ]
