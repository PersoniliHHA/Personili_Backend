from organizations.models import Organization, Workshop, Inventory, InventoryItem, OrganizationProfile, OrganizationMembership, WorkshopMembership
from accounts.factories import AccountFactory, RoleFactory

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
        'website': Faker('url'),
    }

# Organization Factory
class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    business_name = Faker('company')
    legal_name = Faker('company')
    description = Faker('text')
    is_verified = Faker('boolean', chance_of_getting_true=50)
    commerce_registry_number = Faker('random_int', min=1000000000, max=9999999999)
    organization_contact_email = Faker('email')
    organization_contact_phone = Faker('phone_number')


# Organization Profile Factory
class OrganizationProfileFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationProfile

    organization = factory.SubFactory(OrganizationFactory)
    logo_path = Faker('file_path', depth=5, category="image")
    banner_path = Faker('file_path', depth=5, category="image")
    is_sponsored = Faker('boolean', chance_of_getting_true=50)
    head_office_address = Faker('address')
    social_media_links = factory.LazyFunction(lambda: (generate_social_media_links()))

# Organization Membership Factory
class OrganizationMembershipFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationMembership

    organization = factory.SubFactory(OrganizationFactory)
    account = factory.SubFactory(AccountFactory)
    is_active_membership = Faker('boolean', chance_of_getting_true=50)
    role = factory.SubFactory(RoleFactory)


# Workshop Factory
class WorkshopFactory(DjangoModelFactory):
    class Meta:
        model = Workshop

    organization = factory.SubFactory(OrganizationFactory)
    name = Faker('company')
    description = Faker('text')
    is_verified = Faker('boolean', chance_of_getting_true=50)
    commerce_registry_number = Faker('random_int', min=1000000000, max=9999999999)
    contact_email = Faker('email')
    contact_phone = Faker('phone_number')

# Workshop Membership Factory
class WorkshopMembershipFactory(DjangoModelFactory):
    class Meta:
        model = WorkshopMembership

    workshop = factory.SubFactory(WorkshopFactory)
    account = factory.SubFactory(AccountFactory)
    status = Faker('boolean', chance_of_getting_true=50)
    role = factory.SubFactory(RoleFactory)


# Inventory 
class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory
    
    workshop = factory.SubFactory(WorkshopFactory)
    name = Faker('company')
    description = Faker('text')
    address = Faker('address')
    status = Faker('boolean', chance_of_getting_true=50)



# Inventory Item
class InventoryItemFactory(DjangoModelFactory):
    class Meta:
        model = InventoryItem

    inventory = factory.SubFactory(InventoryFactory)
    name = Faker('company')
    description = Faker('text')
    quantity = Faker('random_int', min=1, max=100)
    price = Faker('random_int', min=1, max=1000)
    status = Faker('boolean', chance_of_getting_true=50)
    alert_threshold = Faker('random_int', min=1, max=100)
        