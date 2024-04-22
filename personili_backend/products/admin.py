from django.contrib import admin

# Register your models here.
from products.models import Product, ProductVariant, ProductVariantReview, ProductVariantPreview, DiscountPromotion, AmountPromotion


admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantReview)
admin.site.register(ProductVariantPreview)

admin.site.register(DiscountPromotion)
admin.site.register(AmountPromotion)

