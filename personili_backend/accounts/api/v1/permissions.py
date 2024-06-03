# rest framework imports
from rest_framework import permissions


#################################
#                               #
#     Permission class for      #
#     profile API view-set      #
#                               #
#################################
class ProfileApiPermission(permissions.BasePermission):
    """
    Permissions for Profile API view-set,
    only the owner of the profile can edit it and view it and they must be authenticated.
    """
    message = "You don't have permission to edit or view this profile"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
