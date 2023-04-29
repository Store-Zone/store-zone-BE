from django.contrib import admin

# Register your models here.
from .models import Products
from .models import Carts

admin.site.register(Products)
admin.site.register(Carts)