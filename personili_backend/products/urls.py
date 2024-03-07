# rest framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from personalizables.api.v1.views import CategoryViewSet, PersonalizationTypeViewSet, PersonalizableViewSet

router = DefaultRouter()

urlpatterns = [
 path('', include(router.urls)),
]