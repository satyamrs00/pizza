# Generated by Django 4.0.6 on 2022-07-17 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_cart_price_order_price_subcombination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topping',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
