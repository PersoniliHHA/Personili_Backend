from personalizables.models import Department, Category, Personalizable, PersonalizableOption, PersonalizableVariant, PersonalizableVariantValue, PersonalizableZone, DesignedPersonalizableVariant, DesignedPersonalizableZone, Option, OptionValue, PersonalizationType, PersonalizationMethod
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
     "name": "Phone Cases",
     "description": "Personalizable and designs tailored for Phone Cases",
     "sub_categories": [
            {
                "name": "Iphone Cases",
                "description": "Personalizable and designs tailored for Phone Cases",
                "sub_categories": [
                    { 
                    "name": "iPhone 11 Cases",
                    "description": "Personalizable and designs tailored for Iphone Cases",
                    "sub_categories": []
                    },
                     { 
                    "name": "iPhone 12 Cases",
                    "description": "Personalizable and designs tailored for Iphone Cases",
                    "sub_categories": []
                    }
                ]
            },
            {
                "name": "Samsung Cases",
                "description": "Personalizable and designs tailored for Phone Cases",
                "sub_categories": [
                    { 
                    "name": "Galaxy S20 Cases",
                    "description": "Personalizable and designs tailored for Iphone Cases",
                    "sub_categories": []
                    },
                     { 
                    "name": "Galaxy S21 Cases",
                    "description": "Personalizable and designs tailored for Iphone Cases",
                    "sub_categories": []
                    }
                ]
            },
            {
                "name": "Pixel Cases",
                "description": "Personalizable and designs tailored for Phone Cases",
                "sub_categories": [
                     { 
                    "name": "Galaxy S20 Cases",
                    "description": "Personalizable and designs tailored for Iphone Cases",
                    "sub_categories": []
                    },
                     { 
                    "name": "Galaxy S21 Cases",
                    "description": "Personalizable and designs tailored for Iphone Cases",
                    "sub_categories": []
                    }
                ]
            }
        ]

 },

 {
     "name": "Home & Living",
     "description": "Personalizable and designs tailored for Home & Living",
     "sub_categories": [
         {
             "name": "Bedding",
             "description": "Personalizable and designs tailored for Bedding",
             "sub_categories": [
                    {
                            "name": "Duvet Covers",
                            "description": "Personalizable and designs tailored for Duvet Covers",
                    },
                    {
                            "name": "Pillow Cases",
                            "description": "Personalizable and designs tailored for Pillow Cases",
                    },
                    {
                            "name": "Blankets",
                            "description": "Personalizable and designs tailored for Blankets",
                    },
                    {
                            "name": "Bed Sheets",
                            "description": "Personalizable and designs tailored for Bed Sheets",
                    },
             ]

         },
         {
             "name": "Kitchen & Dining",
             "description": "Personalizable and designs tailored for Kitchen & Dining",
                "sub_categories": [
                        {
                                "name": "Cutting Boards",
                                "description": "Personalizable and designs tailored for Cutting Boards",
                        },
                        {
                                "name": "Mugs",
                                "description": "Personalizable and designs tailored for Mugs",
                        },
                        {
                                "name": "Tea Towels",
                                "description": "Personalizable and designs tailored for Tea Towels",
                        },
                        {
                                "name": "Bowls",
                                "description": "Personalizable and designs tailored for Bowls",
                        },
                ]
         },

     ]
 }
]

DEPARTMENTS_LIST = [
        {
        "name": "Men",
        "description": "Personalizable and designs tailored for Men",
         },
        {"name": "Women",
        "description": "Personalizable and designs tailored fro Women",
        },
        { 
      "name": "Kids",
      "description": "Personalizable and designs tailored for Kids",
        },
        {
        "name": "Baby",
        "description": "Personalizable and designs tailored for Babies",
        },
        {
        "name": "Unisex",
        "description": "Personalizable and designs tailored for Unisex",
        }
]


shape_components = [
{"Rectangle": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Circle": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Triangle": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Square": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Heart": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Star": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Diamond": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Oval": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Hexagon": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}},
{"Pentagon": {
    "x1": 0,
    "y1": 0,
    "x2": 100,
    "y2": 100
}}

]

class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = Faker('word')
    description = Faker('text')
    
    image_path_1 = Faker('image_url')
    image_path_2 = Faker('image_url')
    image_path_3 = Faker('image_url')

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker('word')
    description = Faker('text')
    image_path_1 = Faker('image_url')
    image_path_2 = Faker('image_url')
    image_path_3 = Faker('image_url')

    parent_category = None
    availability_status = "Available"



OPTIONS_AND_VALUES = [
    {
        "name": "Color",
        "values": ["Red", "Blue", "Green", "Yellow", "Black", "White", "Pink", "Purple"]
    },
    {
        "name": "Size",
        "values": ["Small", "Medium", "Large", "Extra Large"]
    },
    {
        "name": "Material",
        "values": ["Cotton", "Polyester", "Leather", "Wool"]
    },
]

class OptionFactory(DjangoModelFactory):
    class Meta:
        model = Option
    
    name = Faker('word')

class OptionValueFactory(DjangoModelFactory):
    class Meta:
        model = OptionValue

    option = factory.SubFactory(OptionFactory)
    value = Faker('word')

class PersonalizationTypeFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizationType

    name = Faker('word')
    description = Faker('text')
    image_path_1 = Faker('image_url')
    image_path_2 = Faker('image_url')
    image_path_3 = Faker('image_url')

class PersonalizationMethodFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizationMethod

    name = Faker('word')
    description = Faker('text')
    personalization_type = factory.SubFactory(PersonalizationTypeFactory)
    image_path_1 = Faker('image_url')
    image_path_2 = Faker('image_url')
    image_path_3 = Faker('image_url')

class PersonalizableFactory(DjangoModelFactory):
    class Meta:
        model = Personalizable

    workshop = None
    name = Faker('sentence')
    description = Faker('text')
    
    brand = Faker('name')
    model = Faker('name')

    category = None
    department = None

    @factory.post_generation
    def related_designs(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for design in extracted:
                self.related_designs.add(design)

    
    is_open_for_personalization = Faker('boolean', chance_of_getting_true=50)

    can_be_template = Faker('boolean', chance_of_getting_true=50)

    used_with_user_uploaded_designs = Faker('boolean', chance_of_getting_true=50)
    used_with_store_designs = Faker('boolean', chance_of_getting_true=50)
    
    used_with_other_workshop_designs = Faker('boolean', chance_of_getting_true=50)
    used_with_same_workshop_designs = Faker('boolean', chance_of_getting_true=50)
    used_with_platform_designs = Faker('boolean', chance_of_getting_true=50)

class PersonalizableZoneFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizableZone
    personalizable = factory.SubFactory(PersonalizableFactory)
    name = Faker('word')
    image_path = Faker('image_url')
    max_nb_designs = Faker('random_int', min=1, max=10)
    x1 = Faker('random_int', min=0, max=100)
    y1 = Faker('random_int', min=0, max=100)
    x2 = Faker('random_int', min=0, max=100)
    y2 = Faker('random_int', min=0, max=100)
    

class PersonalizableOptionFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizableOption
    
    personalizable = factory.SubFactory(PersonalizableFactory)
    option = factory.SubFactory(Option)


class PersonalizableVariantFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizableVariant

    name = Faker('name')
    personalizable = factory.SubFactory(PersonalizableFactory)
    quantity = Faker('random_int', min=1, max=500)

class PersonalizableVariantValueFactory(DjangoModelFactory):
    class Meta:
        model = PersonalizableVariantValue

    personalizable_variant = factory.SubFactory(PersonalizableVariantFactory)
    option_value = factory.SubFactory(OptionValue)
    personalizable_option = factory.SubFactory(PersonalizableOptionFactory)

class DesignedPersonalizableVariantFactory(DjangoModelFactory):
    personalizable_variant = factory.SubFactory(PersonalizableVariantFactory)
    name = Faker('word')

class DesignedPersonalizableZoneFactory(DjangoModelFactory):
    class Meta:
        model = DesignedPersonalizableZone

    designed_personalizable_variant = factory.SubFactory(DesignedPersonalizableVariantFactory)
    personalizable_zone = factory.SubFactory(PersonalizableZoneFactory)

    components = None