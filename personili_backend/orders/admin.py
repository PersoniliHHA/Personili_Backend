from django.contrib import admin

# Register your models here.

# add all orders app models to admin site
from orders.models import Cart, CartItem, Order, OrderItem, Bill, Delivery, DeliveryMethod, DeliveryItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Bill)
admin.site.register(Delivery)
admin.site.register(DeliveryMethod)
admin.site.register(DeliveryItem)


