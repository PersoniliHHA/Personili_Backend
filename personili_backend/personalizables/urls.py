# rest framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from personalizables.api.v1.views import CategoryViewSet, PersonalizationTypeViewSet, PersonalizableViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('personalizations', PersonalizationTypeViewSet, basename='personalization-types')
router.register('personalizables', PersonalizableViewSet, basename='personalizables')

urlpatterns = [
 path('', include(router.urls)),
]
