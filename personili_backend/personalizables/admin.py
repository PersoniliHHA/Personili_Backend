from django.contrib import admin
from personalizables.models import Category, Option, OptionValue
from personalizables.models import PersonalizationType, PersonalizationMethod
from personalizables.models import PersonalizableZone, Personalizable, PersonalizableVariant, PersonalizableOption
from personalizables.models import PersonalizableVariantValue, DesignedPersonalizableVariant, DesignedPersonalizableZone 
from personalizables.models import DesignedPersonalizableZoneRelatedDesign

# Customize option

admin.site.register(Category)
admin.site.register(Option)
admin.site.register(OptionValue)
admin.site.register(PersonalizationType)
admin.site.register(PersonalizationMethod)
admin.site.register(Personalizable)
admin.site.register(PersonalizableZone)
admin.site.register(PersonalizableVariant)
admin.site.register(PersonalizableOption)
admin.site.register(PersonalizableVariantValue)
admin.site.register(DesignedPersonalizableVariant)
admin.site.register(DesignedPersonalizableZone)
admin.site.register(DesignedPersonalizableZoneRelatedDesign)

