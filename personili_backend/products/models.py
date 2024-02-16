# django imports
from django.db import models
from uuid import uuid4
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# local imports
from accounts.models import TimeStampedModel, AccountProfile, DeliveryAddress, PaymentMethod
from designs.models import Store
from personalizables.models import Category, DesignedPersonalizableVariant

# standard imports
from typing import List, Tuple, Dict
from datetime import datetime



#########################################
#             Product model             #
#########################################
class Product(TimeStampedModel):
    """
    product table is linked to :
     - the category table (a product has one and only category)
     - the store table (a product belongs to one and only one store)
     - Personalizable table (a product is one and only one personalizable)
     - price (price of the product)
     - status, it can be either self personalized or store personalized
    """
    SELF_PERSONALIZED = 'For Self'
    STORE_PERSONALIZED = 'For Store'
    PRODUCT_ORIGIN_CHOICES = [
        (SELF_PERSONALIZED, 'For Self'),
        (STORE_PERSONALIZED, 'For Store')
    ]

    PRODUCT_TYPE_CHOICES = [
        ('personalizable', 'Personalizable'),
        ('design', 'Design')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_origin = models.CharField(max_length=255, choices=PRODUCT_ORIGIN_CHOICES, default=SELF_PERSONALIZED)
    product_type = models.CharField(max_length=255, choices=PRODUCT_TYPE_CHOICES, default='personalizable')

    # Define generic foreign key fields
    content_type = models.ForeignKey(ContentType, 
    on_delete=models.CASCADE,
    limit_choices_to={'model__in': ['design', 'designedpersonalizablevariant']}
    )
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name + ' - ' + str(self.id)
    
    
    def get_full_product_description(self):
        """
        This method should return the id, name, price of a product as well as :
        - the name and full profile of the store or the stores that the designs used in this product belong to, this can be obtained through the personalizable zones that are related to the designed personalizable 
        - the full attributes of the designs used in this product, this can be obtained through the personalizable zones that are related to the designed personalizable
        
        """
        # Prepare the response
        response = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'stores': [],
            'designs': []
        }

        # get the full profile of all the stores that the designs used in this product belong to
        for personalizable_zone in self.designed_personalizable.designedpersonalizablezone_set.all():
            pass
    
    def get_stores_names_and_full_profiles(self):
        """
        This method should return the name and full profile of the store or the stores that the designs used in this product belong to, this can be obtained through the personalizable zones that are related to the designed personalizable 
        """
        pass
