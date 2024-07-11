# rest framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

from personalizables.api.v1.views import CategoryViewSet, DepartmentViewSet

router = DefaultRouter()
router.register('v1/personalizables', CategoryViewSet, basename='categories')
router.register('v1/personalizables', DepartmentViewSet, basename='departments')
urlpatterns = [
 path('', include(router.urls)),
]
