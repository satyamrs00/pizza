from argparse import _MutuallyExclusiveGroup
from email.mime import image
from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Pizza(models.Model):
    PIZZA_TYPES = [
        (0, 'Regular'),
        (1, 'Sicilian')
    ]

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pizza_images', blank=True)
    description = models.TextField(blank=True)
    type = models.IntegerField(choices=PIZZA_TYPES, default=0)
    smallprice = models.DecimalField(decimal_places=2, max_digits=10)
    largeprice = models.DecimalField(decimal_places=2, max_digits=10)
    extrascount = models.IntegerField(default=0)

    def getimage(self):
        return self.image
    def getname(self):
        return f"{self.name} {Pizza.PIZZA_TYPES[self.type][1]} Pizza"

class Topping(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class Sub(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='sub_images', blank=True)
    description = models.TextField(blank=True)
    smallprice = models.DecimalField(decimal_places=2, max_digits=10)
    largeprice = models.DecimalField(decimal_places=2, max_digits=10)

    def getimage(self):
        return self.image
    def getname(self):
        return f'{self.name} Sub'

class Addon(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)

class Pasta(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pasta_images', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def getimage(self):
        return self.image
    def getname(self):
        return f'{self.name}'

class Salad(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='salad_images', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def getimage(self):
        return self.image
    def getname(self):
        return f'{self.name}'

class Platter(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='platter_images', blank=True)
    description = models.TextField(blank=True)
    smallprice = models.DecimalField(decimal_places=2, max_digits=10)
    largeprice = models.DecimalField(decimal_places=2, max_digits=10)

    def getimage(self):
        return self.image
    def getname(self):
        return f'{self.name} Dinner Platter'

class User(AbstractUser):
    pass

class PizzaCombination(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="combinations")
    toppings = models.ManyToManyField(Topping)
    size = models.CharField(null=True, max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    def getsize(self):
        return 'S' if self.size == 'small' else 'L'
    def getimage(self):
        return self.pizza.image
    def getname(self):
        return f'{self.pizza.name} {Pizza.PIZZA_TYPES[self.pizza.type][1]} Pizza'

class SubCombination(models.Model):
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="combinations")
    addons = models.ManyToManyField(Addon)
    size = models.CharField(null=True, max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    def getsize(self):
        return 'S' if self.size == 'small' else 'L'
    def getimage(self):
        return self.sub.image
    def getname(self):
        return f'{self.sub.name} Sub'

class PlatterCombination(models.Model):
    platter = models.ForeignKey(Platter, on_delete=models.CASCADE, related_name="combinations")
    size = models.CharField(null=True, max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    
    def getsize(self):
        return 'S' if self.size == 'small' else 'L'
    def getimage(self):
        return self.platter.image
    def getname(self):
        return f'{self.platter.name} Dinner Platter'

class Order(models.Model):
    PAYMENT_MODES = [
        (0, 'UPI'),
        (1, 'Wallets'),
        (2, 'Credit / Debit / ATM Card'),
        (3, 'Net Banking'),
        (4, 'Cash on Delivery')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    pizza = models.ManyToManyField(PizzaCombination, through='OrderPizza', related_name="orders")
    sub = models.ManyToManyField(SubCombination, through='OrderSub', related_name="orders")
    pasta = models.ManyToManyField(Pasta, through='OrderPasta', related_name="orders")
    salad = models.ManyToManyField(Salad, through='OrderSalad', related_name="orders")
    platter = models.ManyToManyField(PlatterCombination, through='OrderPlatter', related_name="orders")
    placedtime = models.DateTimeField(auto_now_add=True)
    completedtime = models.DateTimeField(null=True)
    payment_mode = models.IntegerField(choices=PAYMENT_MODES)
    address = models.ForeignKey('Address', on_delete=models.SET("(deleted address)"))
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    pizza = models.ManyToManyField(PizzaCombination, through='CartPizza', related_name="cart")
    sub = models.ManyToManyField(SubCombination, through='CartSub', related_name="cart")
    pasta = models.ManyToManyField(Pasta, through='CartPasta', related_name="cart")
    salad = models.ManyToManyField(Salad, through='CartSalad', related_name="cart")
    platter = models.ManyToManyField(PlatterCombination, through='CartPlatter', related_name="cart")
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

class WeightedM2M(models.Model):
    datetime_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)

class CartPizza(WeightedM2M):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pizza = models.ForeignKey(PizzaCombination, on_delete=models.CASCADE)

class CartSub(WeightedM2M):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    sub = models.ForeignKey(SubCombination, on_delete=models.CASCADE)

class CartPasta(WeightedM2M):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE)

class CartSalad(WeightedM2M):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    salad = models.ForeignKey(Salad, on_delete=models.CASCADE)

class CartPlatter(WeightedM2M):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    platter = models.ForeignKey(PlatterCombination, on_delete=models.CASCADE)

class OrderPizza(WeightedM2M):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(PizzaCombination, on_delete=models.CASCADE)

class OrderSub(WeightedM2M):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sub = models.ForeignKey(SubCombination, on_delete=models.CASCADE)

class OrderPasta(WeightedM2M):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE)

class OrderSalad(WeightedM2M):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    salad = models.ForeignKey(Salad, on_delete=models.CASCADE)

class OrderPlatter(WeightedM2M):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    platter = models.ForeignKey(PlatterCombination, on_delete=models.CASCADE)

class Address(models.Model):
    name = models.CharField(max_length=200, default="")
    addressline = models.TextField()
    city = models.CharField(max_length=200, default="")
    state = models.CharField(max_length=200, default="")
    country = models.CharField(max_length=200, default="")
    pin = models.PositiveIntegerField(default=0)
    phone = models.CharField(default="", max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)