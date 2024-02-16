from django.contrib import admin

# Register your models here.

# add all orders app models to admin site
from orders.models import Cart, CartItem, Order, OrderItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)


