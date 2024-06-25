# Factories
from designs.models import Design, DesignerProfile, Theme, Store, StoreProfile, Collection, DesignLike, DesignPreview
from accounts.factories import AccountFactory, AccountProfileFactory, generate_social_media_links
from organizations.factories import WorkshopFactory

# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as fk
from random import randint

# python imports
import json

faker_g = fk(['en_US', 'fr_FR', 'ar_AA'])
faker_g.seed_instance(randint(1, 100000))

# DesignerProfile Factory
class DesignerProfileFactory(DjangoModelFactory):
    class Meta:
        model = DesignerProfile

    account_profile = factory.SubFactory(AccountProfileFactory)
    designer_username = faker_g.user_name()
    biography = faker_g.text()
    social_media_website_links = factory.LazyFunction(lambda: json.dumps(generate_social_media_links()))
    designer_logo_path = faker_g.image_url()
    designer_banner_path = faker_g.image_url()
    is_verified = faker_g.boolean(chance_of_getting_true=50)

    tax_number = faker_g.random_int(min=1000000000, max=9999999999)
    registration_number = faker_g.random_int(min=1000000000, max=9999999999)
    registration_date = faker_g.date()
    registration_country = faker_g.country()
    registration_address = faker_g.address()
    registration_certificate_path = faker_g.file_path(depth=5, category="image")


# Store model 
class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store

    name = Faker('company')
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

# Collection Factory
class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection
    name = Faker('word')
    store = factory.SubFactory(StoreFactory)
    workshop = factory.SubFactory(WorkshopFactory)
   

# Design
class DesignFactory(DjangoModelFactory):
    class Meta:
        model = Design

    theme = factory.SubFactory(ThemeFactory)
    title = Faker('word')
    description = Faker('text')
    image_path = Faker('file_path', depth=5, category="image")
    tags = Faker('words')
    # Design type can be either '2d' or '3d',80% chance it's 2d
    design_type = Faker('random_element', elements=('2d', '3d'), chance_of_getting_2d=80)
    # Design status can be either 'pending', 'approved', 'rejected'
    status = Faker('word', ext_word_list=['pending', 'approved', 'rejected'])

    to_be_published = Faker('boolean', chance_of_getting_true=90)

    latest_publication_date = Faker('date')

    collection = factory.SubFactory(CollectionFactory)

    workshop = factory.SubFactory(WorkshopFactory)
    store = factory.SubFactory(StoreFactory)
    regular_user = factory.SubFactory(AccountFactory)
    
    if regular_user:
        to_be_published = False
    
    platform_specific = Faker('boolean', chance_of_getting_true=30)
    # Random float between 0 and 999999
    base_price = Faker('random_float', min=0, max=999999)
    sponsored = Faker('boolean', chance_of_getting_true=30)

    free_usage = Faker('boolean', chance_of_getting_true=50)
    exclusive = Faker('boolean', chance_of_getting_true=50)

    if exclusive:
        free_usage = False
    if not exclusive and not free_usage:
        limited_usage_with_same_collection = Faker('boolean', chance_of_getting_true=50)
        limited_usage_with_same_workshop = Faker('boolean', chance_of_getting_true=50)
        limited_usage_with_same_organization = Faker('boolean', chance_of_getting_true=50)
        limited_usage_with_designer_uploads = Faker('boolean', chance_of_getting_true=50)
        limited_usage_with_user_uploads = Faker('boolean', chance_of_getting_true=50)
        limited_usage_with_other_workshops = Faker('boolean', chance_of_getting_true=50)
        limited_usage_with_other_organizations = Faker('boolean', chance_of_getting_true=50)



class DesignLike(DjangoModelFactory):
    class Meta:
        model = DesignLike

    design = factory.SubFactory(DesignFactory)
    account_profile = factory.SubFactory(AccountProfileFactory)


class DesignPreviewFactory(DjangoModelFactory):
    class Meta:
        model = DesignPreview
    
    design = factory.SubFactory(DesignFactory)
    image_path = Faker('file_path', depth=5, category="image")