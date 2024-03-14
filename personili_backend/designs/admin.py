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
class DesignInline(admin.TabularInline):
    """
    Only the id and the name of the design will be displayed in the collection table
    """
    model = Design
    fields = ['id', 'title', 'status', 'created_at', 'updated_at']


class CollectionAdmin(admin.ModelAdmin):
    inlines = [DesignInline, ]
    extra = 0

# Customize the store table
class CollectionInline(admin.TabularInline):
    model = Collection

class StoreAdmin(admin.ModelAdmin):
    inlines = [CollectionInline, ]


admin.site.register(Store)
admin.site.register(StoreProfile)

admin.site.register(Design, DesignAdmin)

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Theme)
admin.site.register(DesignLike)
admin.site.register(DesignPreview)



