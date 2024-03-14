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
    model = Design

class CollectionAdmin(admin.ModelAdmin):
    inlines = [DesignInline, ]


admin.site.register(Store)
admin.site.register(StoreProfile)

admin.site.register(Design, DesignAdmin)

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Theme)
admin.site.register(DesignLike)
admin.site.register(DesignPreview)



