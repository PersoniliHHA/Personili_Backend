from django.contrib import admin
from accounts.models import User, UserProfile, DeliveryAddress, PaymentMethod, Feedback, Blacklist, Wallet, Transaction

# Add all usermanagement app models to admin site
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(DeliveryAddress)
admin.site.register(PaymentMethod)
admin.site.register(Feedback)
admin.site.register(Blacklist)
admin.site.register(Wallet)
admin.site.register(Transaction)


