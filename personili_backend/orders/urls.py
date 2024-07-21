# rest_framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from orders.api.v1.views import CartViewSet

router = DefaultRouter()
router.register(r'v1/carts', CartViewSet, basename='carts')

urlpatterns = [
    path('', include(router.urls)),
]

