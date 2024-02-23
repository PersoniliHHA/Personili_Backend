from django.contrib import admin
from personalizables.models import PersonalizationType, PersonalizationMethod
from personalizables.models import  PersonalizableZone, Personalizable, PersonalizableVariant, PersonalizableOption
from personalizables.models import PersonalizableVariantValue, DesignedPersonalizableVariant, DesignedPersonalizableZone 
from personalizables.models import  Category, Option, OptionValue
from personalizables.models import  AllowedVariantPersonalizationMethod



admin.register(PersonalizationType)
admin.register(PersonalizationMethod)
admin.register(PersonalizableZone)
admin.register(Personalizable)
admin.register(PersonalizableVariant)
admin.register(PersonalizableOption)
admin.register(PersonalizableVariantValue)
admin.register(DesignedPersonalizableVariant)
admin.register(DesignedPersonalizableZone)
admin.register(Category)
admin.register(Option)
admin.register(OptionValue)
admin.register(AllowedVariantPersonalizationMethod)


