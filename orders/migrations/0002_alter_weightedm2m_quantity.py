# Generated by Django 4.0.6 on 2022-07-24 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weightedm2m',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
