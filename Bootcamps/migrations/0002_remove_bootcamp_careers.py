# Generated by Django 4.2.4 on 2023-08-15 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bootcamps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bootcamp',
            name='careers',
        ),
    ]
