from personalizables.models import Personalizable, PersonalizableOption, PersonalizableVariant, PersonalizableVariantValue, PersonalizableZone, DesignedPersonalizableVariant, DesignedPersonalizableZone
# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as fk
import json
from random import randint

class PersonalizableFactory(DjangoModelFactory):
    class Meta:
        model = Personalizable

    name = Faker('word')
    description = Faker('text')
    is_active = Faker('boolean', chance_of_getting_true=90)