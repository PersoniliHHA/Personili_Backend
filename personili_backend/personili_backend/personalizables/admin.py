from django.contrib import admin
from personalizables.models import Personalizable,  PersonalizableVariant, Category, PersonalizationType, PersonalizationMethod, PersonalizableZone,Color,Size,Material,AllowedPersonalizablesPersonalization, DesignedPersonalizableVariant




admin.site.register(PersonalizationType)
admin.site.register(PersonalizationMethod)
admin.site.register(PersonalizableZone)
admin.site.register(Personalizable)
admin.site.register(PersonalizableVariant)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Material)
admin.site.register(AllowedPersonalizablesPersonalization)

