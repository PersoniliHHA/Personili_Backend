from organizations.models import BusinessOwnerProfile,Organization, OrganizationProfile,  Workshop, Inventory, InventoryItem, OrganizationMembership, WorkshopMembership
from django.contrib import admin



# Add all usermanagement app models to admin site
admin.site.register(BusinessOwnerProfile)
admin.site.register(Organization)
admin.site.register(Workshop)
admin.site.register(Inventory)
admin.site.register(InventoryItem)
admin.site.register(OrganizationProfile)
admin.site.register(OrganizationMembership)
admin.site.register(WorkshopMembership)



