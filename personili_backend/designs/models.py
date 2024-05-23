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
from organizations.models import Workshop

# Utils
from utils.constants import DESIGNER_UPLOADED_IMAGES_PATH_TEMPLATES
from utils.utilities import add_to_dict


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
    an image path,
    a status,
    list of tags,
    a price,
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

    _3D = "3d"
    _2D = "2d"
    DESIGN_TYPES = [
        (_3D, '3D'),
        (_2D, '2D'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
   
    # General attributes 
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='design')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    design_type = models.CharField(max_length=255, choices=DESIGN_TYPES, default=_2D)
    
    # Design initial status is PENDING, eventually it becomes either APPROVED or REJECTED
    status = models.CharField(max_length=255, choices=STATUS, default=PENDING)
    # Designs uploaded by the user are not to be published, designers or workshops can choose to or not to publish them
    to_be_published = models.BooleanField(default=False)
    
    latest_publication_date = models.DateTimeField(null=True, blank=True)
    
    # Optionally the design can be linked to a collection
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='designs', null=True, blank=True)


    # a design can only be linked either a workshop or a store or a regular user
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='designs', null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='designs', null=True, blank=True)
    regular_user = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, related_name='designs', null=True, blank=True)
    
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # free design
    free = models.BooleanField(default=False)

    # sponsored design
    sponsored = models.BooleanField(default=False)

    ###### Usage and exclusivity parameters #######
    ## the following two parameters are mutually exclusive, if one is true the other should be false

    # 1- Free usage with other designs, this is valid by default for designs uploaded by the designer
    free_usage = models.BooleanField(default=False) # This parameter cancels the other parameters
    # 2- Exclusive usage, the design can only be used alone 
    exclusive_usage = models.BooleanField(default=False) # this parameter cancels the other parameters

    ## The following parameters are only valid if the exclusive_usage is set to False
    ## If all of these parameters are set to True, then that's the equiviliant of free usage
    limited_usage_with_same_collection = models.BooleanField(default=False)
    limited_usage_with_same_workshop = models.BooleanField(default=False)
    limited_usage_with_same_organization = models.BooleanField(default=False)
    limited_usage_with_designer_uploads = models.BooleanField(default=False)
    limited_usage_with_user_uploads = models.BooleanField(default=False)
    limited_usage_with_other_workshops = models.BooleanField(default=False)
    limited_usage_with_other_organizations = models.BooleanField(default=False)

    # override the save method to check for attributes consistency
    def save(self, *args, **kwargs):
        # Check that the design is linked to either a store or a workshop or a regular user
        if not self.store and not self.workshop and not self.regular_user:
            raise ValueError('A design should be linked to either a store or a workshop or a regular user')
        
        # Check the exclusivity and usage parameters
        # if the uploader is a designer then the design is free by default
        if self.regular_user:
            self.workshop = None
            self.store = False
            self.free_usage = False
            self.exclusive_usage = True

        elif self.store:
            self.free_usage = True
            self.workshop = None
            self.regular_user = None
        elif self.workshop:
            self.store = None
            self.regular_user = None

            if self.exclusive_usage:
                self.free_usage = False
                self.free_usage_with_same_collection = False
                self.free_usage_with_same_workshop = False
                self.free_usage_with_same_organization = False
                self.free_usage_with_designer_uploads = False
                self.free_usage_with_user_uploads = False
                self.free_usage_with_other_organizations = False
                self.free_usage_with_other_workshops = False
            if self.free_usage:
                self.exclusive_usage = False
                self.free_usage_with_same_collection = True
                self.free_usage_with_same_workshop = True
                self.free_usage_with_same_organization = True
                self.free_usage_with_designer_uploads = True
                self.free_usage_with_user_uploads = True
                self.free_usage_with_other_organizations = True
                self.free_usage_with_other_workshops = True
            if self.free :
                self.base_price = 0.0
        
        if self.base_price == 0.0:
            self.free = True


        super(Design, self).save(*args, **kwargs)

    class Meta:
        db_table = 'designs'

    def __str__(self):
        return self.title + " - " + str(self.id)
    
    @classmethod
    def get_designs(cls, 
                        theme_ids= None,
                        store_ids=None,
                        workshop_ids=None,
                        organization_ids=None,
                        promotion_ids=None,

                        sponsored_designs=False,
                        sponsored_stores=False,
                        search_term=None,
                        tags=None,
                        
                        free = None,
                        price_min=None,
                        price_max=None,
                        latest_publication_date_min=None,
                        latest_publication_date_max=None,
                        
                        offset=0,
                        limit=20): 
        """
        This method returns the most popular designs (the ones that were approved and not uploaded by a regular user)
        compute the number of likes per design and return the top "limit" designs
        for each design we get :
        - id
        - title
        - theme name
        - image_path
        - store name or workshop name and its organization name depending on which one is not null
        - number of likes
        - design preview objects


        Filters used : 
        - theme_ids : list of theme ids
        - store_ids : list of store ids
        - workshop_ids : list of workshop ids
        - organization_ids : list of organization ids
        - sponsored_designs : boolean
        - search_term : string
        - tags : list of tags
        - promotion_ids : list of promotion ids
        - free : boolean
        - price_min : float
        - price_max : float
        - latest_publication_date_min : datetime
        - latest_publication_date_max : datetime
        - offset : int
        - limit : int
        """
        q_objects = Q()
        # First filter the designs which are approved and to be published
        q_objects.add(Q(status=cls.APPROVED, to_be_published=True), Q.AND)
        # Filter the designs which don't belong to a regular user
        q_objects.add(Q(regular_user=None), Q.AND)

        # price filters
        if free:
            q_objects.add(Q(price=0.0), Q.AND)
        if price_min:
            q_objects.add(Q(base_price__gte=price_min), Q.AND)
        if price_max:
            q_objects.add(Q(base_price__lte=price_max), Q.AND)

        # filter by theme, store, workshop, organization, sponsored stores, sponsored organizations
        if theme_ids:
            q_objects.add(Q(theme_id__in=theme_ids), Q.AND)
        if store_ids:
            q_objects.add(Q(collection__store_id__in=store_ids), Q.AND)
        if workshop_ids:
            q_objects.add(Q(collection__workshop_id__in=workshop_ids), Q.AND)
        if organization_ids:
            q_objects.add(Q(collection__workshop__organization_id__in=organization_ids), Q.AND)

        # Date filters
        if latest_publication_date_min:
            q_objects.add(Q(latest_publication_date__gte=latest_publication_date_min), Q.AND)
        if latest_publication_date_max:
            q_objects.add(Q(latest_publication_date__lte=latest_publication_date_max), Q.AND)

        # Tags filter
        if tags:
            for tag in tags:
                q_objects.add(Q(tags__icontains=tag), Q.AND)

        # filter sponsored designs
        if sponsored_designs:
            q_objects.add(Q(sponsored=True), Q.AND)

        # search for the search term in the title, the description, the tags of the design, also the theme name and description, the store name and organization name
        if search_term:
            q_objects.add(Q(title__icontains=search_term) | 
                          Q(description__icontains=search_term) | 
                          Q(tags__icontains=search_term) | 
                          Q(theme__name__icontains=search_term) | 
                          Q(theme__description__icontains=search_term) | 
                          Q(store__name__icontains=search_term) |
                          Q(store__storeprofile__biography__icontains=search_term) |
                          Q(workshop__organization__name__icontains=search_term) |
                          Q(workshop__organization__orgprofile__biography__icontains=search_term) |
                          Q(workshop__name__icontains=search_term), Q.AND)
            
        designs = (cls.objects.filter(q_objects)
                           .annotate(num_likes=models.Count('design_likes')) 
                           .select_related('store__storeprofile', 'workshop__organization__orgprofile', 'theme')
                           .prefetch_related('design_previews')
                           .order_by('-num_likes')[offset:offset+limit])
        result = {"designs_list":[]}
        for design in designs:
            # Root dict to contain design data
            design_data = {
                "design_id": design.id,
            }
            # Design details
            design_details = {
                'design_title': design.title,
                'design_description': design.description,
                'design_theme_id': design.theme.id,
                'design_theme_name': design.theme.name,
                'design_image_path': design.image_path,
                'design_nb_likes': design.num_likes,
                'design_previews': list(design.design_previews.values('id', 'image_path')),
                'design_tags': design.tags,
                'design_price': design.base_price,
                'latest_publication_date': design.latest_publication_date,
            }
            design_data['design_details'] = design_details
            
            # Design owner
            design_owner = {}
            if design.store:
                design_owner = {
                    'store_name': design.store.name,
                    'store_id': design.store.id,
                    'store_verified': design.store.storeprofile.is_verified,
                    'store_sponsored': design.store.storeprofile.is_sponsored,
                }
            elif design.workshop:
                design_owner = {
                    'workshop_name': design.workshop.name,
                    'workshop_id': design.workshop.id,
                    'organization_name': design.workshop.organization.name,
                    'organization_id': design.workshop.organization.id,
                    'organization_sponsored': design.workshop.organization.orgprofile.is_sponsored,
                }
            design_data['design_owner'] = design_owner

            # Design usage parameters
            design_usage_parameters = {}
            if design.exclusive_usage:
                design_usage_parameters = {
                    'exclusive_usage': design.exclusive_usage,
                }
            elif design.free_usage:
                design_usage_parameters = {
                    'free_usage': design.free_usage,
                }
            else:
                design_usage_parameters = {
                    'free_usage_with_same_collection': design.free_usage_with_same_collection,
                    'free_usage_with_same_workshop': design.free_usage_with_same_workshop,
                    'free_usage_with_same_organization': design.free_usage_with_same_organization,
                    'free_usage_with_designer_uploads': design.free_usage_with_designer_uploads,
                    'free_usage_with_user_uploads': design.free_usage_with_user_uploads,
                    'free_usage_with_other_workshops': design.free_usage_with_other_workshops,
                    'free_usage_with_other_organizations': design.free_usage_with_other_organizations,
                }
            design_data['design_usage_parameters'] = design_usage_parameters
            result['designs_list'].append(design_data)

        result["count"] = designs.count()
        
        return result
    
    @classmethod
    def get_full_design_details(cls, design_id:str):
        """
        This method returns all the infos related to a specific design :
        - design id
        - design title
        - design description
        - design image path
        - design tags
        - design price
        - design theme id and name
        - design exclusive or not
        - design store id and name and logo or workshop id and name and organization name and logo
        """
        
        design = (cls.objects.filter(id=design_id, status=cls.APPROVED, to_be_published=True, regular_user=None)
                                    .select_related('store__store_profile', 'workshop__organization', 'theme')
                                    .prefetch_related('design_previews')
                                    .annotate(num_likes=models.Count('design_likes'))
                                    .first())
        
        design_details: dict = {}
        
        return design_details
    
    def like(self, account_profile: AccountProfile):
        """
        This method is used to like a design, it creates a design like object
        """
        DesignLike.objects.create(design=self, account_profile=account_profile)
    
    def unlike(self, account_profile: AccountProfile):
        """
        This method is used to unlike a design, it deletes the design like object
        """
        DesignLike.objects.filter(design=self, account_profile=account_profile).delete()

    def is_liked_by(self, account_profile: AccountProfile):
        """
        This method checks if a design is liked by a specific user
        """
        return DesignLike.objects.filter(design=self, account_profile=account_profile).exists()

    #  
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