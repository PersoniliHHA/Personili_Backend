# rest_framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from designs.api.views import DesignsViewSet

router = DefaultRouter()
router.register(r'designs', DesignsViewSet, basename='designs')

urlpatterns = [
    path('', include(router.urls)),
]

