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


#################################
#                               #
#     Permission class for      #
#     Delivery address          #
#     API view-set              #
#                               #
#################################
class PrivateDeliveryAddressApiPermission(permissions.BasePermission):
    """
    Permissions for Delivery Address API view-set, only the owner of the profile to which the delivery address is related
    can edit it and view it, and they must be authenticated.
    """
    message = "You don't have permission to edit or view this delivery address"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user


#################################
#                               #
#     Permission class for      #
#     Private Wallet            #
#     API view-set              #
#                               #
#################################
class PrivateWalletApiPermission(permissions.BasePermission):
    """
    Permission for Private Wallet API view-set, only the owner of the profile to which the wallet is related
    can edit it and view it, and they must be authenticated.
    """
    message = "You don't have permission to edit or view this wallet"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user
