from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Pizza)
admin.site.register(models.Topping)
admin.site.register(models.Sub)
admin.site.register(models.Addon)
admin.site.register(models.Pasta)
admin.site.register(models.Salad)
admin.site.register(models.Platter)
admin.site.register(models.User)
