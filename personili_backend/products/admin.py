from django.contrib import admin

# Register your models here.
from products.models import Product, ProductReview, DiscountPromotion, AmountPromotion, CodePromotion


admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(DiscountPromotion)
admin.site.register(AmountPromotion)
admin.site.register(CodePromotion)

