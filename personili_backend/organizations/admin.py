from organizations.models import Organization, OrganizationProfile,  Workshop, Inventory, InventoryItem, OrganizationMembership
from django.contrib import admin



# Add all usermanagement app models to admin site
admin.site.register(Organization)
admin.site.register(Workshop)
admin.site.register(Inventory)
admin.site.register(InventoryItem)
admin.site.register(OrganizationProfile)
admin.site.register(OrganizationMembership)



