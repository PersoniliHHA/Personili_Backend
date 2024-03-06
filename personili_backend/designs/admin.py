from django.contrib import admin

# add all designs app models to admin site
from designs.models import Store, Design, Theme, StoreProfile, Collection, DesignLike, DesignPreview


admin.site.register(Store)
admin.site.register(StoreProfile)
admin.site.register(Design)
admin.site.register(Collection)
admin.site.register(Theme)
admin.site.register(DesignLike)
admin.site.register(DesignPreview)

