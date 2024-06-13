# Factories
from designs.models import Design, DesignerProfile, Theme, Store, StoreProfile, Collection, DesignLike, DesignPreview
from accounts.factories import AccountFactory, generate_social_media_links

# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory

# python imports
import json

# DesignerProfile Factory
class DesignerProfileFactory(DjangoModelFactory):
    class Meta:
        model = DesignerProfile

    account = factory.SubFactory(AccountFactory)
    biography = Faker('text')
    social_media_links = factory.LazyFunction(lambda: json.dumps(generate_social_media_links()))
    designer_logo_path = Faker('file_path', depth=5, category="image")
    designer_banner_path = Faker('file_path', depth=5, category="image")
    designer_website = Faker('url')
    designer_verified = Faker('boolean', chance_of_getting_true=50)

    tax_number = Faker('random_int', min=1000000000, max=9999999999)
    registration_number = Faker('random_int', min=1000000000, max=9999999999)
    registration_date = Faker('date')
    registration_country = Faker('country')
    registration_certificate_path = Faker('file_path', depth=5, category="image")


# Store model 
class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store

    store_name = Faker('company')
    designer_profile = factory.SubFactory(DesignerProfileFactory)

# StoreProfile Factory
class StoreProfileFactory(DjangoModelFactory):
    class Meta:
        model = StoreProfile

    store = factory.SubFactory(StoreFactory)
    biography = Faker('text')
    store_logo_path = Faker('file_path', depth=5, category="image")
    store_banner_path = Faker('file_path', depth=5, category="image")
    is_sponsored = Faker('boolean', chance_of_getting_true=50)

# Theme Factory
class ThemeFactory(DjangoModelFactory):
    class Meta:
        model = Theme

    name = Faker('word')
    description = Faker('text')
    icon_path = Faker('file_path', depth=5, category="image")

# DesignLike
class DesignLikeFactory(DjangoModelFactory):
    class Meta:
        model = DesignLike

    design = factory.SubFactory(DesignFactory)
    account = factory.SubFactory(AccountFactory)