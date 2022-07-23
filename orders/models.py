from cgi import print_exception
from tkinter import CASCADE
from unicodedata import name
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import AbstractUser

PIZZA_TYPES = [
    (0, 'Regular'),
    (1, 'Sicilian')
]

ORDER_STATUS = [
    (0, 'placed'),
    (1, 'completed')
]

# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=200)
    type = models.IntegerField(choices=PIZZA_TYPES, default=0)
    smallprice = models.DecimalField(decimal_places=2, max_digits=10)
    largeprice = models.DecimalField(decimal_places=2, max_digits=10)
    extrascount = models.IntegerField(default=0)

class Topping(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class Sub(models.Model):
    name = models.CharField(max_length=200)
    smallprice = models.DecimalField(decimal_places=2, max_digits=10)
    largeprice = models.DecimalField(decimal_places=2, max_digits=10)

class Addon(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)

class Pasta(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)

class Salad(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)

class Platter(models.Model):
    name = models.CharField(max_length=200)
    smallprice = models.DecimalField(decimal_places=2, max_digits=10)
    largeprice = models.DecimalField(decimal_places=2, max_digits=10)

class User(AbstractUser):
    pass

class PizzaCombination(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="combinations")
    toppings = models.ManyToManyField(Topping)
    size = models.CharField(null=True, max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class SubCombination(models.Model):
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="combinations")
    addons = models.ManyToManyField(Addon)
    size = models.CharField(null=True, max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class PlatterCombination(models.Model):
    platter = models.ForeignKey(Platter, on_delete=models.CASCADE, related_name="combinations")
    size = models.CharField(null=True, max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    pizza = models.ManyToManyField(PizzaCombination, related_name="orders")
    sub = models.ManyToManyField(SubCombination, related_name="orders")
    pasta = models.ManyToManyField(Pasta, related_name="orders")
    salad = models.ManyToManyField(Salad, related_name="orders")
    platter = models.ManyToManyField(PlatterCombination, related_name="orders")
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    pizza = models.ManyToManyField(PizzaCombination, related_name="cart")
    sub = models.ManyToManyField(SubCombination, related_name="cart")
    pasta = models.ManyToManyField(Pasta, related_name="cart")
    salad = models.ManyToManyField(Salad, related_name="cart")
    platter = models.ManyToManyField(PlatterCombination, related_name="cart")
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
