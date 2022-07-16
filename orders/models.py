from unicodedata import name
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import AbstractUser

PIZZA_TYPES = [
    (0, 'Regular'),
    (1, 'Sicilian')
]

# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=200)
    type = models.IntegerField(choices=PIZZA_TYPES, default=0)
    smallprice = models.DecimalField(decimal_places=2, max_digits=10)
    largeprice = models.DecimalField(decimal_places=2, max_digits=10)

class Topping(models.Model):
    name = models.CharField(max_length=200)

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