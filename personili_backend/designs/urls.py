# rest_framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from designs.api.v1.views import DesignsViewSet

router = DefaultRouter()
router.register(r'v1/designs', DesignsViewSet, basename='designs')

urlpatterns = [
    path('', include(router.urls)),
]

