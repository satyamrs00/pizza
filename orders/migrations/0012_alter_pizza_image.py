# Generated by Django 4.0.6 on 2022-08-08 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_pizza_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]