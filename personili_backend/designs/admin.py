from django.contrib import admin

# add all designs app models to admin site
from designs.models import Store, Design, Theme, StoreProfile, Collection, DesignLike, DesignPreview

"""

# Customize the collection table
# for each collection, display the designs in the collection
class DesignInline(admin.StackedInline):
    model = Design
    readonly_fields = ['id']
    extra = 0


class CollectionAdmin(admin.ModelAdmin):
    inlines = [DesignInline, ]

# Customize the store table
class CollectionInline(admin.StackedInline):
    model = Collection
    readonly_fields = ['id']
    extra = 0

class StoreAdmin(admin.ModelAdmin):
    inlines = [CollectionInline, ]

"""
admin.site.register(Store)
admin.site.register(StoreProfile)
admin.site.register(Design)
admin.site.register(Collection)
admin.site.register(Theme)
admin.site.register(DesignLike)
admin.site.register(DesignPreview)



