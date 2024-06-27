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
    is_2d_ = Faker('boolean', chance_of_getting_true=80)
    if is_2d_:
        design_type = '2d'
    else:
        design_type = '3d'
    
    status_prob = randint(1, 100)
    if status_prob <= 80:
        chosen_status = 'approved'
    elif status_prob > 80 and status_prob <= 90:
        chosen_status = 'pending'
    else:
        chosen_status = 'rejected'
    # Design status can be either 'pending', 'approved', 'rejected'
    status = chosen_status

    workshop = factory.SubFactory(WorkshopFactory)
    store = factory.SubFactory(StoreFactory)
    regular_user = factory.SubFactory(AccountFactory)
    
    if workshop or store:
        to_be_published = Faker('boolean', chance_of_getting_true=90)
        latest_publication_date = Faker('date')

    if regular_user:
        to_be_published = False
        latest_publication_date = None
    
    # Random float between 0 and 999999
    if workshop or store:
        base_price = Faker('random_float', min=0, max=999999)
        sponsored = Faker('boolean', chance_of_getting_true=30)

    if regular_user:
        base_price = 0
        sponsored = False
        free_usage = True
    else:
        free_usage = Faker('boolean', chance_of_getting_true=50)
        exclusive_usage = Faker('boolean', chance_of_getting_true=50)

        if exclusive_usage:
            free_usage = False
            limited_usage_with_designer_uploads = False
            limited_usage_with_user_uploads = False
            limited_usage_with_other_workshops = False
            limited_usage_with_other_organizations = False
            limited_usage_with_same_collection = False
            limited_usage_with_same_workshop = False
            limited_usage_with_same_organization = False

        elif free_usage:
            exclusive_usage = False
            limited_usage_with_designer_uploads = False
            limited_usage_with_user_uploads = False
            limited_usage_with_other_workshops = False
            limited_usage_with_other_organizations = False
            limited_usage_with_same_collection = False
            limited_usage_with_same_workshop = False
            limited_usage_with_same_organization = False

        else:
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