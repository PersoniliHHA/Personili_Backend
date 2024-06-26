from accounts.models import Account, AccountProfile, AccountBlacklist, DeliveryAddress, Permission, Role, RoleAccount, RolePermission
import factory
from factory import Faker
from factory.django import DjangoModelFactory
import json
from faker import Faker as fk
from random import randint

fake = fk()
# Create faker object with 3 languages as providers : english, french and arabic
faker_g = fk(['en_US', 'fr_FR', 'ar_AA'])
faker_g.seed_instance(randint(1, 1000000))

emails_set = set()

def generate_unique_email():
    email = faker_g.email()
    while email in emails_set:
        email = faker_g.email()
    emails_set.add(email)
    return email

################## Account Factory #########################
class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    email = factory.LazyFunction(generate_unique_email)
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email_verified = Faker('boolean', chance_of_getting_true=90)
    is_active = Faker('boolean', chance_of_getting_true=90)
    is_staff = Faker('boolean', chance_of_getting_true=0)
    is_superuser = Faker('boolean', chance_of_getting_true=0)
    is_admin = Faker('boolean', chance_of_getting_true=0)


################## Account Profile Factory ##################
def generate_social_media_links():
    return {
        'facebook': fake.url(),
        'twitter': fake.url(),
        'instagram': fake.url(),
        'linkedin': fake.url(),
        'pinterest': fake.url(),
        'youtube': fake.url(),
        'tiktok': fake.url(),
    }
class AccountProfileFactory(DjangoModelFactory):
    class Meta:
        model = AccountProfile

    account = factory.SubFactory(AccountFactory)
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = Faker('user_name')
    phone_number = Faker('phone_number')
    
    profile_picture_path = Faker('image_url')
    date_of_birth = Faker('date_of_birth')
    gender = faker_g.random_element(elements=('Male', 'Female', 'Not specified'))
    
    biography = Faker("text")
    social_media_links = factory.LazyFunction(lambda: json.dumps(generate_social_media_links()))


class DeliveryAddressFactory(DjangoModelFactory):
    class Meta:
        model = DeliveryAddress

    account_profile = factory.SubFactory(AccountFactory)
    street = Faker('street_address')
    city = Faker('city')
    zip_code = Faker('postcode')
    state = Faker('state')
    country = Faker("country")
    is_default = Faker('boolean', chance_of_getting_true=50)

class PermissionFactory(DjangoModelFactory):
    class Meta:
        model = Permission

    name = Faker('word')
    description = Faker('text')


class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role

    name = Faker('word')
    description = Faker('text')
    permissions = factory.SubFactory(PermissionFactory)