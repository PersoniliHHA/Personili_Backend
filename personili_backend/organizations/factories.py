from organizations.models import Organization, Workshop, Inventory, InventoryItem, OrganizationProfile, OrganizationMembership, WorkshopMembership
from accounts.factories import AccountFactory, RoleFactory

# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as fk
import json
fake = fk()

def generate_social_media_links():
    return {
        'facebook': fake.url(),
        'twitter': fake.url(),
        'instagram': fake.url(),
        'linkedin': fake.url(),
        'pinterest': fake.url(),
        'youtube':fake.url(),
        'tiktok':fake.url(),
        'website': fake.url(),
    }

# Organization Factory
class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    account = factory.SubFactory(AccountFactory)
    business_name = Faker('company')
    legal_name = Faker('company')
    description = Faker('text')
    is_verified = Faker('boolean', chance_of_getting_true=50)

    tax_number = Faker('random_int', min=1000000000, max=9999999999)
    registration_number = Faker('random_int', min=1000000000, max=9999999999)
    registratioin_date = Faker('date')
    registration_country = Faker('country')
    registration_certificate_path = Faker('file_path', depth=5, category="image")

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
    social_media_links = factory.LazyFunction(lambda: (json.dumps(generate_social_media_links())))

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
    description = Faker('text', length=255)
    is_active = Faker('boolean', chance_of_getting_true=50)
    contact_email = Faker('email')
    contact_phone = Faker('phone_number')
    address = Faker('address', length=255)

# Workshop Membership Factory
class WorkshopMembershipFactory(DjangoModelFactory):
    class Meta:
        model = WorkshopMembership

    workshop = factory.SubFactory(WorkshopFactory)
    account = factory.SubFactory(AccountFactory)
    is_active_membership = Faker('boolean', chance_of_getting_true=50)
    role = factory.SubFactory(RoleFactory)


# Inventory 
class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory
    
    workshop = factory.SubFactory(WorkshopFactory)
    name = Faker('company')
    description = Faker('text')
    status = Faker('random_element', elements=('empty', 'partially_full', 'full'))



# Inventory Item
class InventoryItemFactory(DjangoModelFactory):
    class Meta:
        model = InventoryItem

    inventory = factory.SubFactory(InventoryFactory)
    name = Faker('company')
    sku = Faker('pystr', min_chars=10, max_chars=30)
    description = Faker('text')
    quantity = Faker('random_int', min=1, max=100)
    base_price = Faker('random_int', min=1, max=1000)
    alert_threshold = Faker('random_int', min=1, max=100)
        