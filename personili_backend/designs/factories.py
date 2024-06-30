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
import random

# python imports
import json

faker_g = fk(['en_US', 'fr_FR', 'ar_AA'])
faker_g.seed_instance(randint(1, 100000))

# DesignerProfile Factory
class DesignerProfileFactory(DjangoModelFactory):
    class Meta:
        model = DesignerProfile

    account_profile = factory.SubFactory(AccountProfileFactory)
    designer_username = Faker('user_name')
    biography = Faker('text')
    social_media_website_links = factory.LazyFunction(lambda: json.dumps(generate_social_media_links()))
    designer_logo_path = faker_g.image_url()
    designer_banner_path = faker_g.image_url()
    is_verified = faker_g.boolean(chance_of_getting_true=50)

    tax_number = Faker('random_int', min=1000000000, max=9999999999)
    registration_number = Faker('random_int', min=1000000000, max=9999999999)
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
    icon_1_path = Faker("image_url")
    icon_2_path = Faker("image_url")
    icon_3_path = Faker("image_url")

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
    image_path = Faker("image_url")
    tags = Faker('words')
    
    # Design type can be either '2d' or '3d',80% chance it's 2d
    @factory.lazy_attribute
    def design_type(self):
        return random.choices(['2d', '3d'], weights=[0.8, 0.2], k=1)[0]
    
    @factory.lazy_attribute
    def status(self):
        # Define your choices and their associated probabilities
        choices = ['approved', 'pending', 'rejected']
        probabilities = [0.8, 0.1, 0.1]  # 80%, 10%, 10% probabilities
        # Use random.choices() to select one of the statuses based on the specified probabilities
        return random.choices(choices, weights=probabilities, k=1)[0]

    # Design status can be either 'pending', 'approved', 'rejected'

    workshop = factory.SubFactory(WorkshopFactory)
    store = factory.SubFactory(StoreFactory)
    regular_user = factory.SubFactory(AccountProfileFactory)
    collection = factory.SubFactory(CollectionFactory)

    latest_publication_date = Faker('date')
    to_be_published = Faker('boolean', chance_of_getting_true=90)
    base_price = Faker('random_float', min=0, max=999999)
    sponsored = Faker('boolean', chance_of_getting_true=30)
    free_usage = Faker('boolean', chance_of_getting_true=50)
    exclusive_usage = Faker('boolean', chance_of_getting_true=50)
    limited_usage_with_designer_uploads = Faker('boolean', chance_of_getting_true=50)
    limited_usage_with_user_uploads = Faker('boolean', chance_of_getting_true=50)
    limited_usage_with_other_workshops = Faker('boolean', chance_of_getting_true=50)
    limited_usage_with_other_organizations = Faker('boolean', chance_of_getting_true=50)
    limited_usage_with_same_collection = Faker('boolean', chance_of_getting_true=50)
    limited_usage_with_same_workshop = Faker('boolean', chance_of_getting_true=50)
    limited_usage_with_same_organization = Faker('boolean', chance_of_getting_true=50)



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