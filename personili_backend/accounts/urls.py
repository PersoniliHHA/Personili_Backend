# rest framework imports
from rest_framework.routers import DefaultRouter

# Django imports
from django.urls import path, include

from .api.v1.views import AccountAuthViewSet

############################## Router for User Management API ##############################

router = DefaultRouter()
# Account management APIs
## Public user management APIs
router.register('accounts', AccountAuthViewSet, basename='accounts')
#router.register('signin', PublicUserSignInViewSet, basename='signin')
#router.register('feedback', PublicFeedbackViewSet, basename='feedback')

## Private user management APIs
#router.register('signout', PrivateUserSignOutViewSet, basename='signout')
#router.register('profile', PrivateProfileViewSet, basename='profile')
#router.register('delivery-address', DeliveryAddressViewSet, basename='delivery-address')
#router.register('payment-method', PrivateProfileViewSet, basename='payment-method')
#router.register('blacklist', PrivateProfileViewSet, basename='blacklist')
#router.register('wallet', PrivateWalletViewSet, basename='wallet')

# Workshops APIs
## Public designs APIs
## Private designs APIs

urlpatterns = [
    path('', include(router.urls)),

]
