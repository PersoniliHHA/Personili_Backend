from personalizables.models import Departement, Category, Personalizable, PersonalizableOption, PersonalizableVariant, PersonalizableVariantValue, PersonalizableZone, DesignedPersonalizableVariant, DesignedPersonalizableZone

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


class PersonalizableVariantFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizableVariant

    name = Faker('word')

