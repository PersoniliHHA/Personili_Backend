# rest framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from personalizables.api.views import CategoryViewSet, PersonalizationTypeViewSet, PersonalizableViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'personalizations', PersonalizationTypeViewSet, basename='personalization-types')
router.register(r'personalizables', PersonalizableViewSet, basename='personalizables')

urlpatterns = [
 path('', include(router.urls)),
]
