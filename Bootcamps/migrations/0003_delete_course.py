# Generated by Django 4.2.4 on 2023-08-15 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bootcamps', '0002_remove_bootcamp_careers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Course',
        ),
    ]
