from products.models import Product, ProductVariant, ProductVariantPreview, ProductVariantReview
from personalizables.factories import DesignedPersonalizableVariantFactory, DepartmentFactory, CategoryFactory
from organizations.factories import WorkshopFactory, OrganizationFactory
from accounts.factories import AccountFactory, AccountProfileFactory

# factory boy imports
import factory
from factory import Faker
from factory.django import DjangoModelFactory
from factory import SubFactory
from faker import Faker as fk
import json
from random import randint


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    title = Faker('sentence', nb_words=4)
    description = Faker('text')
    workshop = SubFactory(WorkshopFactory)
    category = SubFactory(CategoryFactory)
    department = SubFactory(DepartmentFactory)
    user = SubFactory(AccountProfileFactory)
    self_made = Faker('boolean')
    to_be_published = Faker('boolean', chance_of_getting_true=90)
    latest_publication_date = Faker('date')
    editable = Faker('boolean', chance_of_getting_true=10)

class ProductVariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = SubFactory(ProductFactory)
    designed_personalizable_variant = SubFactory(DesignedPersonalizableVariantFactory)

    name = Faker('word')
    description = Faker('text')
    price = Faker('random_int', min=1, max=1000)
    quantity = Faker('random_int', min=1, max=1000)

    sku = Faker('ean13')


class ProductVariantPreviewFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariantPreview

    product_variant = SubFactory(ProductVariantFactory)
    image_path = Faker("image_url")

class ProductVariantReviewFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariantReview

    product_variant = SubFactory(ProductVariantFactory)
    account_profile = SubFactory(AccountProfileFactory)
    rating = Faker('random_int', min=1, max=5)
    comment = Faker('text')
  