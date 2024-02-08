# DRF imports
from rest_framework import permissions
# local imports
from designs.models import Store


class IsStoreOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        store_id = view.kwargs['store_id']

        profile = user.profile
        store = Store.objects.get(id=store_id)

        return user.is_authenticated and profile.store == store
