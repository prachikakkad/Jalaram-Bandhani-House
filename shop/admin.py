from django.contrib import admin
from .models import Product, Message, Order, Order_Update, Review

# Register your models here.

admin.site.register((Product, Message, Order, Order_Update, Review))