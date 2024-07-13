# rest framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from personalizables.api.v1.views import CategoryViewSet, DepartmentViewSet, PersonalizableViewSet

router = DefaultRouter()
router.register('v1/personalizables', CategoryViewSet, basename='categories')
router.register('v1/personalizables', DepartmentViewSet, basename='departments')
router.register('v1/personalizables', PersonalizableViewSet, basename='personalizables')
urlpatterns = [
 path('', include(router.urls)),
]
