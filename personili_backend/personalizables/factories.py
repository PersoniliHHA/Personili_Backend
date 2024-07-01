from personalizables.models import Departement, Category, Personalizable, PersonalizableOption, PersonalizableVariant, PersonalizableVariantValue, PersonalizableZone, DesignedPersonalizableVariant, DesignedPersonalizableZone, Option, OptionValue, PersonalizationType, PersonalizationMethod
from designs.factories import DesignFactory

# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from factory import SubFactory
from faker import Faker as fk
import json
from random import randint

CATEGORIES_LIST = [
 {
     
 }
]

class DepartementFactory(DjangoModelFactory):
    class Meta:
        model = Departement

    name = Faker('word')
    description = Faker('text')
    
    image_path_1 = Faker('image_url')
    image_path_2 = Faker('image_url')
    image_path_3 = Faker('image_url')

class Category(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker('word')
    description = Faker('text')
    image_path_1 = Faker('image_url')
    image_path_2 = Faker('image_url')
    image_path_3 = Faker('image_url')

    parent_category = None
    availability_status = None

class Option(DjangoModelFactory):
    class Meta:
        model = Option
    
    name = Faker('word')

class OptionValue(DjangoModelFactory):
    class Meta:
        model = OptionValue

    option = factory.SubFactory(Option)
    value = Faker('word')

class PersonalizationType(DjangoModelFactory):
    class Meta:
        model = PersonalizationType

    name = Faker('word')
    description = Faker('text')
    image_path_1 = Faker('image_url')
    image_path_2 = Faker('image_url')
    image_path_3 = Faker('image_url')

class PersonalizationMethod(DjangoModelFactory):
    class Meta:
        model = PersonalizationMethod

    name = Faker('word')
    description = Faker('text')
    personalization_type = factory.SubFactory(PersonalizationType)
    image_path_1 = Faker('image_url')
    image_path_2 = Faker('image_url')
    image_path_3 = Faker('image_url')

class PersonalizableFactory(DjangoModelFactory):
    class Meta:
        model = Personalizable

    name = Faker('word')
    description = Faker('text')
    
    brand = Faker('word')
    model = Faker('word')

    category = None
    departement = None

    @factory.post_generation
    def related_designs(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for design in extracted:
                self.related_designs.add(design)

    
    is_open_for_personalization = Faker('boolean', chance_of_getting_true=50)

    can_be_template = Faker('boolean', chance_of_getting_true=50)

    used_with_designers_designs = Faker('boolean', chance_of_getting_true=50)
    used_with_user_uploaded_designs = Faker('boolean', chance_of_getting_true=50)
    used_with_store_designs = Faker('boolean', chance_of_getting_true=50)
    used_with_workshop_designs = Faker('boolean', chance_of_getting_true=50)


class PersonalizableZoneFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizableZone
    personalizable = factory.SubFactory(Personalizable)
    name = Faker('word')
    image_path = Faker('image_url')
    max_nb_designs = Faker('random_int', min=1, max=10)
    x1 = Faker('random_int', min=0, max=100)
    y1 = Faker('random_int', min=0, max=100)
    x2 = Faker('random_int', min=0, max=100)
    y2 = Faker('random_int', min=0, max=100)
    

class PersonalizableOption(DjangoModelFactory):
    class Meta:
        model = PersonalizableOption
    
    personalizable = factory.SubFactory(Personalizable)
    option = factory.SubFactory(Option)


class PersonalizableVariantFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizableVariant

    name = Faker('word')
    personalizable = factory.SubFactory(Personalizable)
    quantity = Faker('random_int', min=1, max=100)

class PersonalizableVariantValueFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizableVariantValue

    personalizable_variant = factory.SubFactory(PersonalizableVariant)
    option_value = factory.SubFactory(OptionValue)
    personalizable_option = factory.SubFactory(PersonalizableOption)

class DesignedPersonalizableVariantFactory(DjangoModelFactory):
    personalizable_variant = factory.SubFactory(PersonalizableVariant)
    name = Faker('word')

class DesignedPersonalizableZone(DjangoModelFactory):
    class Meta:
        model = DesignedPersonalizableZone

    designed_personalizable_variant = factory.SubFactory(DesignedPersonalizableVariantFactory)
    personalizable_zone = factory.SubFactory(PersonalizableZoneFactory)
    design = factory.SubFactory(DesignFactory)

    dx1 = Faker('random_int', min=0, max=100)
    dy1 = Faker('random_int', min=0, max=100)
    dx2 = Faker('random_int', min=0, max=100)
    dy2 = Faker('random_int', min=0, max=100)