# Standard libraries
from uuid import uuid4
from enum import Enum

# Django
from django.db import models
from django.core import serializers
from django.db.models import Q

# Models
from accounts.models import AccountProfile
from accounts.models import TimeStampedModel
from personalizables.models import PersonalizableVariant
from organizations.models import Workshop

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
        return self.account_profile.account.email + " - " + self.name
    
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
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='storeprofile')
    biography = models.TextField(null=True, blank=True)
    store_logo_path = models.CharField(max_length=255, null=True, blank=True)
    store_banner_path = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)


    class Meta:
        db_table = 'store_profiles'

    def __str__(self):
        return self.store.account_profile.account.email + " - " + self.store.name
    
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
    Every collection can be either linked to a store or a workshop
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=255, default="My Collection")
    
    # only one of the two fields should be filled
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='collection', null=True, blank=True, default=None)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='collection', null=True, blank=True, default=None)
    
    class Meta:
        db_table = 'collections'

    def save(self, *args, **kwargs):
        if self.store and self.workshop:
            raise ValueError('A collection can only be linked to a store or a workshop, not both')
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + ' - ' + self.name

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
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    logo_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'themes'

    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
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
                              default=PENDING)
    
    # This field is used to determine if the design should be published or not on our website
    to_be_published = models.BooleanField(default=True)

    # Can the design be used with other designs from other designers
    exclusive_usage = models.BooleanField(default=True)

    # Is the design limited to a certain number of personalizables
    limited_personalizables = models.BooleanField(default=False)

    class Meta:
        db_table = 'designs'

    def __str__(self):
        return self.title + " - " + str(self.id)
    
    @classmethod
    def get_designs_light(cls, 
                                  theme_id= None,
                                  store_id=None,
                                  workshop_id=None,
                                  sponsored_stores=False,
                                  sponsored_organizations=False,
                                  search_term=None,
                                  limit=20, 
                                  offset=0):
        """
        This method returns the most popular designs (the ones that were approved)
        compute the number of likes per design and return the top "limit" designs
        for each design we get :
        - id
        - title
        - image_path
        - store name or workshop name and its organization name depending on which one is not null
        - number of likes
        - design preview objects
        """
        q_objects = Q()
        if theme_id:
            q_objects.add(Q(theme_id=theme_id), Q.AND)
        if store_id:
            q_objects.add(Q(collection__store_id=store_id), Q.AND)
        if workshop_id:
            q_objects.add(Q(collection__workshop_id=workshop_id), Q.AND)
        if sponsored_stores and sponsored_organizations:
            q_objects.add(Q(collection__store__storeprofile__is_sponsored=True) |
                          Q(collection__workshop__organization__orgprofile__is_sponsored=True), Q.AND)
        else:
            if sponsored_organizations and not sponsored_stores:
                q_objects.add(Q(collection__workshop__organization__orgprofile__is_sponsored=True), Q.AND)
            if sponsored_stores and not sponsored_organizations:
                q_objects.add(Q(collection__store__storeprofile__is_sponsored=True), Q.AND)

        # search for the search term in the title, the description, the tags of the design, also the theme name and description, the store name and organization name
        if search_term:
            q_objects.add(Q(title__icontains=search_term) | 
                          Q(description__icontains=search_term) | 
                          Q(tags__icontains=search_term) | 
                          Q(theme__name__icontains=search_term) | 
                          Q(theme__description__icontains=search_term) | 
                          Q(collection__store__name__icontains=search_term) | 
                          Q(collection__workshop__name__icontains=search_term), Q.AND)
            
        popular_designs = (cls.objects.filter(status=cls.APPROVED, to_be_published=True)
                           .filter(q_objects)
                           .annotate(num_likes=models.Count('design_likes')) 
                           .select_related('collection__store', 'collection__workshop__organization', 'theme')
                           .prefetch_related('design_previews')
                           .order_by('-num_likes')[offset:offset+limit])
        result = []
        for design in popular_designs:
            design_data = {
                'design_id': design.id,
                'design_title': design.title,
                'design_theme': design.theme.name,
                'design_description': design.description,
                'design_image_path': design.image_path,
                'store_name': design.collection.store.name if design.collection.store else None,
                'store_verified': design.collection.store.storeprofile.is_verified if design.collection.store else None,
                'store_sponsored': design.collection.store.storeprofile.is_sponsored if design.collection.store else None,
                'workshop_name': design.collection.workshop.name if design.collection.workshop else None,
                'organization_name': design.collection.workshop.organization.name if design.collection.workshop else None,
                'organization_sponsored': design.collection.workshop.organization.orgprofile.is_sponsored if design.collection.workshop else None,
                'design_nb_likes': design.num_likes,
                'design_previews': list(design.design_previews.values('id', 'image_path'))
            }
            # remove None values from the dictionary
            design_data = {k: v for k, v in design_data.items() if v is not None}
            result.append(design_data)
        
        return result
    
    @classmethod
    def get_full_design_details(cls, design_id:str):
        """
        """
        pass


#########################################
#        Design likes model             #
#########################################
class DesignLike(TimeStampedModel):
    """
    This model is used to store the likes of a design
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='design_likes')
    account_profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, related_name='design_likes')

    class Meta:
        db_table = 'design_likes'
        unique_together = ('design', 'account_profile')

    def __str__(self):
        return self.design.title + " - " + self.account_profile.account.email
    


#########################################
#        Design previews model          #
#########################################
class DesignPreview(TimeStampedModel):
    """
    This model is used to store the previews of a design
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='design_previews')
    image_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'design_previews'

    def __str__(self):
        return self.design.title + " - " + str(self.id)