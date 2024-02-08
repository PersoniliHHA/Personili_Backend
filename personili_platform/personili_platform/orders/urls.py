# rest_framework imports
from rest_framework.routers import DefaultRouter

# django imports
from django.urls import path, include

# define the router
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]