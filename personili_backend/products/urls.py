# rest framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from products.api.v1.views import ProductViewSet

router = DefaultRouter()
router.register(r'v1/products', ProductViewSet, basename='products')


urlpatterns = [
 path('', include(router.urls)),
]