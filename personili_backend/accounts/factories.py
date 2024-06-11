from accounts.models import Account, AccountProfile, AccountBlacklist, DeliveryAddress, Permission, Role, RoleAccount, RolePermission
import factory
from factory import Faker
from factory.django import DjangoModelFactory
import json

################## Account Factory #########################
class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    email = Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email_verified = Faker('boolean', chance_of_getting_true=50)
    is_active = Faker('boolean', chance_of_getting_true=50)
    is_staff = Faker('boolean', chance_of_getting_true=50)
    is_superuser = Faker('boolean', chance_of_getting_true=50)


################## Account Profile Factory ##################
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
class AccountProfileFactory(DjangoModelFactory):
    class Meta:
        model = AccountProfile

    account = factory.SubFactory(AccountFactory)
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = Faker('user_name')
    phone_number = Faker('phone_number')
    profile_picture_path = Faker('file_path', depth=3, category="image")
    date_of_birth = Faker('date')
    gender = Faker('random_element', elements=('Male', 'Female', 'Not specified'))
    biography = Faker('text')
    #social_media_links = factory.LazyFunction(lambda: json.dumps(generate_social_media_links()))