# Generated by Django 4.0.6 on 2022-08-08 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_pizza_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
