from django.contrib import admin

# add all designs app models to admin site
from designs.models import Store, Design, Theme, StoreProfile, Collection, DesignLike, DesignPreview

# Add filter vertical to many to many field in the design table
class DesignMemberInline(admin.TabularInline):
    model = Design.personalizable_variants.through


class DesignAdmin(admin.ModelAdmin):
    inlines = [DesignMemberInline, ]
    exclude = ['personalizable_variants']

# Customize the collection table
# for each collection, display the designs in the collection
class DesignInline(admin.StackedInline):
    """
    Only the id and the name of the design will be displayed in the collection table
    """
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


admin.site.register(Store, StoreAdmin)
admin.site.register(StoreProfile)

admin.site.register(Design, DesignAdmin)

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Theme)
admin.site.register(DesignLike)
admin.site.register(DesignPreview)



