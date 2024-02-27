# Standard libraries
from uuid import uuid4
from enum import Enum

# Django
from django.db import models

# Models
from accounts.models import AccountProfile
from accounts.models import TimeStampedModel
from personalizables.models import PersonalizableVariant

# Utils
from utils.constants import DESIGNER_UPLOADED_IMAGES_PATH_TEMPLATES
from utils.utilities import store_image_in_s3


#########################################
#             Store model               #
#########################################
class Store(TimeStampedModel):
    """
    Model for a store, it has an id, a name, 
    a biography and is linked to one and only one user profile
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    # user can can have many stores linked to its profile
    account_profile = models.ForeignKey(AccountProfile, on_delete=models.DO_NOTHING, related_name='store')

    class Meta:
        db_table = 'stores'

    def __str__(self):
        return self.user_profile.user.email + " - " + self.name
    
    def get_full_store_profile(self):
        """
        Returns all the attributes in the store profile related to this store, the store profile has 
        """
        full_store_profile = {
            'store': self,
            'store_profile': self.store_profile,
            'collections': self.get_related_collections(),
            'collections_and_designs': self.get_collections_and_their_designs(),
        }


    def get_related_collections(self):
        """Get the collections related to this store"""
        return self.collection_set.all()

    def get_collections_and_their_designs(self):
        """
        Returns a list of collections related to this store and the designs of each collection
        """
        collections = self.get_related_collections()
        collections_and_designs = []
        for collection in collections:
            collections_and_designs.append({
                'collection': collection,
                'designs': collection.get_designs()
            })
        return collections_and_designs
    

#########################################
#           Store profile model         #
#########################################
class StoreProfile(TimeStampedModel):
    """
    Every store has one and only one profile, the profile has the following fields:
    - id
    - store (one to one relationship)
    - type (personal, verified, sponsored)
    - store_logo
    - store_banner
    - biography
    - store_logo_path
    - store_banner_path
    - is_trending
    - is_bestseller
    - is_featured
    - is_upcoming
    """
    ## Type choices
    PERSONAL = "personal"
    VERIFIED = "Verified"
    SPONSORED = "Sponsored"
    TYPE = [
        (PERSONAL, 'Personal'),
        (VERIFIED, 'Verified'),
        (SPONSORED, 'Sponsored'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='store_profile')
    type = models.CharField(max_length=255, choices=TYPE, default=PERSONAL)
    biography = models.TextField(null=True, blank=True)
    store_logo_path = models.CharField(max_length=255, null=True, blank=True)
    store_banner_path = models.CharField(max_length=255, null=True, blank=True)
    is_trending = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=False)

    class Meta:
        db_table = 'store_profiles'

    def __str__(self):
        return self.store.user_profile.user.email + " - " + self.store.name
    
    def get_store_products(self):
        """
        This method searches for all the products that belong to the store, it returns a list of products
        Each product is linked to a store
        """


#########################################
#             Collection model          #
#########################################
class Collection(TimeStampedModel):
    """
    Every collection belongs to one and only one store, it has a title, a description, a list of tags
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='collection')
    title = models.CharField(max_length=255, default="My Collection")
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'collections'

    def __str__(self):
        return str(self.id) + ' - ' + self.title

    def get_designs(self):
        """Get the designs related to this collection, the design table has a foreign key to collection"""
        return Design.objects.filter(collection=self)
        

    
#########################################
#             Theme model               #
#########################################
class Theme(TimeStampedModel):
    """
    Every design belong to one and only one theme, it has a title, a description, a logo
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    logo_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'themes'

    def __str__(self):
        return str(self.id) + ' - ' + self.title
    
    def get_designs_and_their_stores_related_to_this_theme(self):
        pass



#########################################
#             Design model              #
#########################################

class Design(TimeStampedModel):
    """
    Every Design belong to one and only one collection, it has one theme as well
    it has a title,
    a description,
    a picture,
    a status,
    list of tags
    """
    ## Status choices
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUS = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='design')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='design')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255,
                              choices=STATUS,
                              default=APPROVED)
    
    # This field is used to determine if the design should be published or not on our website
    to_be_published = models.BooleanField(default=True)

    # Can the design be used with other designs from other designers
    exclusive = models.BooleanField(default=True)

    # Is the design limited to a certain number of personalizables
    limited_personalizables = models.BooleanField(default=False)

    class Meta:
        db_table = 'designs'

    def __str__(self):
        return self.title + " - " + str(self.id)
    

    @classmethod
    def create_new_design(cls, user_profile,
                               serializer,
                               to_be_published=True):
        """
        This method creates a new design:
        - First it creates the initial design, then store the image in the S3 bucket, then it creates the designed personalizable
        """
       
        # Create the design
        design = Design(
            title=serializer.validated_data.get('title'),
            description=serializer.validated_data.get('description'),
            theme=Theme.objects.get(id=serializer.validated_data.get('theme')),
            collection=Collection.objects.get(pk=serializer.validated_data.get('collection')),
            tags=serializer.validated_data.get('tags'),
            to_be_published=to_be_published,
        )
      
        # Store the image path in the S3 bucket
        image = serializer.validated_data.get('image')
        placeholders = {
            "designer_id": str(user_profile.user.id),
            "designer_email": user_profile.user.email,
            "collection_id": serializer.validated_data.get('collection'),
            "collection_title": Collection.objects.get(id=serializer.validated_data.get('collection')).title,
            "design_id": str(design.id),
            "design_title": serializer.validated_data.get('title')
        }
        image_path = DESIGNER_UPLOADED_IMAGES_PATH_TEMPLATES.get("uploaded_designs").format(**placeholders)
        presigned_image_url = store_image_in_s3(image, image_path)

        design.image_path = image_path
        design.save()
        
        return design.id, presigned_image_url
    
    @classmethod
    def get_designs_by_theme(cls):
        pass

    @classmethod
    def get_designs_by_collection(cls):
        pass 

    def get_products_where_this_design_is_used(self):
        """
        This method returns a list of products where this design is used
        - We need to loop through the designed zones of each designed personalizable and 
        """
        pass
        

    