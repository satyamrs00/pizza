from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Pizza, models.Topping, models.Sub, models.Addon, models.Pasta, models.Salad, models.Platter)
class MenuAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('completedtime',)