# Generated by Django 4.0.6 on 2022-08-05 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_emailsent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailSent',
        ),
    ]
