# Generated by Django 5.1.7 on 2025-03-25 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0014_homepagequestion_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagequestion',
            name='answer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='homepagequestion',
            name='question',
            field=models.CharField(max_length=255),
        ),
    ]
