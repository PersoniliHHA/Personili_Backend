from django.contrib import admin
from accounts.models import Account, AccountProfile, DeliveryAddress, PaymentMethod, Feedback, AccountBlacklist, Wallet, Transaction, RolePermission, Role, Permission

# Add all usermanagement app models to admin site
admin.site.register(Account)
admin.site.register(AccountProfile)
admin.site.register(RolePermission)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(DeliveryAddress)
admin.site.register(PaymentMethod)
admin.site.register(Feedback)
admin.site.register(AccountBlacklist)
admin.site.register(Wallet)
admin.site.register(Transaction)


