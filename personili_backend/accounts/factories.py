from accounts.models import Account, AccountProfile, AccountBlacklist, DeliveryAddress, Permission, Role, RoleAccount, RolePermission
import factory
from factory import Faker
from factory.django import DjangoModelFactory
import json
from faker import Faker as fk

fake = fk()
# Create faker object with 3 languages as providers : english, french and arabic
faker_g = fk(['en_US', 'fr_FR', 'ar_AA'])

################## Account Factory #########################
class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    email = faker_g.email()
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email_verified = faker_g.boolean(chance_of_getting_true=50)
    is_active = faker_g.boolean(chance_of_getting_true=50)
    is_staff = faker_g.boolean(chance_of_getting_true=0)
    is_superuser = faker_g.boolean(chance_of_getting_true=0)
    is_admin = faker_g.boolean(chance_of_getting_true=0)


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
    first_name = faker_g.first_name()
    last_name = faker_g.last_name()
    username = faker_g.user_name()
    phone_number = faker_g.phone_number()
    
    profile_picture_path = faker_g.image_url()
    date_of_birth = faker_g.date_of_birth()
    gender = faker_g.random_element(elements=('Male', 'Female', 'Not specified'))
    
    biography = faker_g.text()
    social_media_links = factory.LazyFunction(lambda: json.dumps(generate_social_media_links()))


class DeliveryAddressFactory(DjangoModelFactory):
    class Meta:
        model = DeliveryAddress

    account_profile = factory.SubFactory(AccountFactory)
    street = faker_g.address()
    city = faker_g.city()
    zip_code = faker_g.postcode()
    state = faker_g.state()
    country = faker_g.country()
    is_default = faker_g.boolean(chance_of_getting_true=50)

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