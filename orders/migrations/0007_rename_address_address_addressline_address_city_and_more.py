# Generated by Django 4.0.6 on 2022-07-28 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_completedtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address',
            new_name='addressline',
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='address',
            name='pin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default='', max_length=200),
        ),
    ]
