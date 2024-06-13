from organizations.models import Organization, Workshop, OrganizationProfile, OrganizationMembership, WorkshopMembership
from accounts.models import Account, AccountProfile

# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory

def generate_social_media_links():
    return {
        'facebook': Faker('url'),
        'twitter': Faker('url'),
        'instagram': Faker('url'),
        'linkedin': Faker('url'),
        'pinterest': Faker('url'),
        'youtube': Faker('url'),
        'tiktok': Faker('url'),
    }

# Organization Factory
class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = Faker('company')
    description = Faker('text')
    is_verified = Faker('boolean', chance_of_getting_true=50)
    commerce_registry_number = Faker('random_int', min=1000000000, max=9999999999)
    main_contact_email = Faker('email')
    main_contact_phone = Faker('phone_number')
    main_address = Faker('address')


# Organization Profile Factory
class OrganizationProfileFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationProfile

    organization = factory.SubFactory(OrganizationFactory)
    logo_path = Faker('file_path', depth=5, category="image")
    banner_path = Faker('file_path', depth=5, category="image")
    is_sponsored = Faker('boolean', chance_of_getting_true=50)

    address = Faker('address')
    social_media_links = factory.LazyFunction(lambda: (generate_social_media_links()))