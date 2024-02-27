# Standard libraries
from uuid import uuid4

# Django
from django.db import models
from django.db.models import Count
from django.forms.models import model_to_dict

# Models
from accounts.models import TimeStampedModel
from organizations.models import InventoryItem

# Utilities
from utils.utilities import get_presigned_url_for_image


#########################################
#             Category model            #
#########################################
class Category(TimeStampedModel):
    """
    Category model,
    each category has a name and a description and a picture,
    and a parent category, root categories have no parent category
    Status: can be either Available/Unavailable/Hidden/ComingSoon
    """
    AVAILABILITY_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
        ('Hidden', 'Hidden'),
        ('ComingSoon', 'ComingSoon')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    logo_path = models.CharField(max_length=255, null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    availability_status = models.CharField(max_length=255, choices=AVAILABILITY_STATUS_CHOICES, default='Unavailable')

    class Meta:
        db_table = 'Categories'

    def __str__(self):
        return self.name + " - " + str(self.id)
    
    def get_direct_parent_category(self):
        return self.parent_category
    
    def get_direct_subcategories(self):
        return Category.objects.filter(parent_category=self)
    
    def get_top_parent_category(self):
        """
        This method returns the top parent category of this category
        """
        if self.parent_category:
            return self.parent_category.get_top_parent_category()
        else:
            return self
    
    @classmethod
    def get_category_tree(cls, parent_category=None):
        """
        This method returns teh entire category tree under a specific parent category, if the parent
        category is null then the method returns the entire category tree
        """
        categories = Category.objects.filter(parent_category=parent_category)
        category_tree = []
        for category in categories:
            if category.availability_status == 'Available' or category.availability_status == 'ComingSoon':
                category_dict = {}
                category_dict["id"] = category.id
                category_dict["name"] = category.name
                category_dict["description"] = category.description
                category_dict["image_path"] = category.image_path
                category_dict["sub_categories"] = cls.get_category_tree(category.id)
                category_tree.append(category_dict)
        
        return category_tree

########################################################
#                Options and values                    #
########################################################
class Option(TimeStampedModel):
    """
    Each option has a name and a description
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Options'

    def __str__(self):
        return self.name + " - " + str(self.id)

class OptionValue(TimeStampedModel):
    """
    Each option value is linked to one and only one option, 
    it has a name and a description
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='option_values')
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'OptionValues'

    def __str__(self):
        return self.value + " - " + str(self.id)

#########################################
#       PersonalizationType model       #
#########################################
class PersonalizationType(TimeStampedModel):
    """
    A personalization type has a name and a description and a logo path and an image path 
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    logo_path = models.CharField(max_length=255, null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'PersonalizationTypes'

    def __str__(self):
        """
        Returns the name of the personalization type
        """
        return self.name + " - " + str(self.id)
    
    @classmethod
    def get_all_personalization_types(cls):
        """
        This method should return a list of dictionaries, each dictionary contain the name, description, logo and image of the personalization type
        """
        personalization_types = [
            {   
                'id': personalization_type.id,
                'name': personalization_type.name,
                'description': personalization_type.description,
                'logo_path': get_presigned_url_for_image(personalization_type.logo_path),
                'image_path': get_presigned_url_for_image(personalization_type.image_path)
            } for personalization_type in PersonalizationType.objects.all()
        ]
        return personalization_types
    
    @classmethod
    def get_all_personaliation_types_with_related_personalization_methods(cls):
        """
        This method should return a list of nested dictionaries, each dictionary contain the name, description, logo and image of the personalization type
        and another dictionary containing id, name and description of the personalization method of this particular personlization type
        """
        personalization_types = [
            {   
                'id': personalization_type.id,
                'name': personalization_type.name,
                'description': personalization_type.description,
                'logo_path': get_presigned_url_for_image(personalization_type.logo_path),
                'image_path': get_presigned_url_for_image(personalization_type.image_path),
                'personalization_methods': [
                    {
                        'id': personalization_method.id,
                        'name': personalization_method.name,
                        'description': personalization_method.description,
                        'logo_path': get_presigned_url_for_image(personalization_method.logo_path),
                        'image_path': get_presigned_url_for_image(personalization_method.image_path)
                    } for personalization_method in PersonalizationMethod.objects.filter(personalization_type=personalization_type)
                ]
            } for personalization_type in PersonalizationType.objects.all()
        ]
        return personalization_types

    def get_related_personalization_methods(self):
        """
        """
        return self.personalization_method.all()
    
    @classmethod
    def get_allowed_personalizables_and_their_zones_for_personalization_type(cls, personalization_type_id):
        """
        This method returns a list of ids of personalizables that are allowed for this personalization type
        """
        response: List[dict]= []
        # Get the list of allowed personalizables ids for this personalization type
        personalizables_ids: List[str] = []
        allowed_personalizables = AllowedPersonalizablesPersonalization.objects.filter(personalization_type=personalization_type_id)
        personalizables_ids = [allowed_personalizable.personalizable.id for allowed_personalizable in allowed_personalizables]

        # Get the list of personalizable zones and variants (colors, sizes, materials) for each personalizable
        for personalizable_id in personalizables_ids:
            
            # get the personalizable object
            personalizable = Personalizable.objects.get(pk=personalizable_id)
            if personalizable.availability:
                # first get the personalizable and its attributes
                response.append({
                    "id": personalizable_id,
                    "name": personalizable.name,
                    "description": personalizable.description,
                    "category_id": personalizable.category.id,
                    "category_name": Category.objects.get(pk=personalizable.category.id).name,
                    "variants": personalizable.get_variants_of_a_personalizable(),
                    "zones": personalizable.get_personalizable_zones_of_a_personalizable()
                })
            
        return response
        

#########################################
#         PersonalizationMethod model   #
#########################################
class PersonalizationMethod(TimeStampedModel):
    """
    A personalization method has a name and a description and a logo, every personalization method is linked to a personalization type
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalization_type = models.ForeignKey(PersonalizationType, on_delete=models.CASCADE, related_name='personalization_method')
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    logo_path = models.CharField(max_length=255, null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'PersonalizationMethods'

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_personalization_method_logo(self):
        return self.logo

#########################################
#         Personalizable model          #
#########################################
class Personalizable(TimeStampedModel):
    """
    A printable model has a name, 
    a type, 
    a description, 
    an image path,
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, default="Generic Brand")
    model = models.CharField(max_length=255, null=True, default="Generic Model")

    class Meta:
        db_table = 'Personalizables'


    def __str__(self):
        return self.name + " - " + self.category.name + " - " + str(self.id)
    
    def get_variants_of_a_personalizable(self):
        """
        This method takes the id of a personalizable and returns a list of colors, sizes and materials available for this personalizable
        - It first gets the personalizable variants lines in the personalizable variant table, then retrieves all the colors, sizes and materials using their ids
        and returns them in a list of dictionaries
        """
        response = []
        personalizable_variants = self.variants.all()
        
        for variant in personalizable_variants:
            response.append({
                'variant_id': variant.id,
                'stock_quantity': variant.stock_quantity
            })
        return response
    
    def get_personalizable_zones_of_a_personalizable(self):
        """
        This method takes the id of a personalizable and 
        returns a list of personalizable zones
        """
        response = []
        personalizable_zones = self.zones.all()
        for personalizable_zone in personalizable_zones:
            response.append({
                'personalizable_id': personalizable_zone.id,
                'name': personalizable_zone.name,
                'image_url': get_presigned_url_for_image(personalizable_zone.image_path),
                'default_display': personalizable_zone.default_display,
                'maximum_number_of_designs_allowed': personalizable_zone.maximum_number_of_designs,
                'dx': personalizable_zone.dx,
                'dy': personalizable_zone.dy,
                'dh': personalizable_zone.dh,
                'dw': personalizable_zone.dw,
                'x1': personalizable_zone.x1,
                'y1': personalizable_zone.y1,
                'x2': personalizable_zone.x2,
                'y2': personalizable_zone.y2
            })
        return response

#########################################
#     PersonalizableOption model        #
#########################################
class PersonalizableOption(TimeStampedModel):
    """
    A personalizable option is linked to a personalizable with an option
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable = models.ForeignKey(Personalizable, on_delete=models.CASCADE, related_name='options')
    option = models.ForeignKey('Option', on_delete=models.CASCADE, related_name='personalizables')

    class Meta:
        db_table = 'PersonalizableOptions'

    def __str__(self):
        return self.personalizable.name + " - " + self.option.name + " - " + str(self.id)


#########################################
#       PersonalizableZone model        #
#########################################
class PersonalizableZone(TimeStampedModel):
    """
    - A personalizable zone is linked to one and only one personalizable but a personalizable can have many zones, 
    it has an id, 
    a name, 
    an image path and coordinates dx, dy, dh, dw, x1, y1, x2, y2
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable = models.ForeignKey(Personalizable, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=255, null=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    default_display = models.BooleanField(default=False)
    maximum_number_of_designs = models.IntegerField(null=True)
    dx = models.FloatField(null=True)
    dy = models.FloatField(null=True)
    dh = models.FloatField(null=True)
    dw = models.FloatField(null=True)
    x1 = models.FloatField(null=True)
    y1 = models.FloatField(null=True)
    x2 = models.FloatField(null=True)
    y2 = models.FloatField(null=True)

    class Meta:
        db_table = 'PersonalizableZones'

    def __str__(self):
        return self.personalizable.name + " - " + self.name

#########################################
#      PersonalizableVariant model      #
#########################################
class PersonalizableVariant(TimeStampedModel):
    """
    A personalizable variant is linked to a sku in the inventory item table and to a personalizable
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable = models.ForeignKey(Personalizable, on_delete=models.CASCADE, related_name='variants')
    sku = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='personalizable_variants')

    class Meta:
        db_table = 'PersonalizableVariants'

    def get_the_variant_values(self):
        """
        This method returns the option values of this personalizable variant
        """
        pass


#########################################
#    PersonalizableVariantValue model   #
#########################################
class PersonalizableVariantValue(TimeStampedModel):
    """
    A personalizable variant value is linked to :
    - a personalizable variant
    - an option value
    - a personalizable option
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable_variant = models.ForeignKey(PersonalizableVariant, on_delete=models.CASCADE, related_name='option_values')
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE, related_name='personalizable_variants')
    personalizable_option = models.ForeignKey(PersonalizableOption, on_delete=models.CASCADE, related_name='personalizable_variants')
    
    class Meta:
        db_table = 'PersonalizableVariantValues'

    def __str__(self):
        return self.personalizable_variant.personalizable.name + " - " + self.option_value.name + " - " + str(self.id)

########################################################
#  Allowed personalizable/personalization methd model  #
########################################################
class AllowedVariantPersonalizationMethod(TimeStampedModel):
    """
    Associates the id of the personalizable and the id of the allowed personalization type
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable = models.ForeignKey(Personalizable, on_delete=models.CASCADE, related_name='allowed_personalizables')
    personalization_method = models.ForeignKey(PersonalizationMethod, on_delete=models.CASCADE, related_name='allowed_personalizables')
    
    class Meta:
        db_table = 'AllowedVariantPersonalizationMethods'

    def __str__(self):
        return self.personalizable.name + " - " + str(self.id)

########################################################
#                Designed variant model                #
########################################################
class DesignedPersonalizableVariant(TimeStampedModel):
    """
    A designed personalizable variant is linked to:
     - a personalizable variant 
     -
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable_variant = models.ForeignKey(PersonalizableVariant, on_delete=models.CASCADE, related_name='designed_personalizable_variant')
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'DesignedPersonalizableVariants'

########################################################
#                Designed Zone model                   #
########################################################
class DesignedPersonalizableZone(TimeStampedModel):
    """
    A designed personalizable zone is linked to a personalizable zone, 
    it has an id and a foreign key to a personalizable zone and foreign key to the designed personalizable variant and a foreign key to the 
    design table
    and also 4 coordinates dx, dy, dh, dw
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable_zone = models.ForeignKey(PersonalizableZone, on_delete=models.CASCADE, related_name='designed_personalizable_zone')
    designed_personalizable_variant = models.ForeignKey(DesignedPersonalizableVariant, on_delete=models.CASCADE, related_name='designed_personalizable_zone')
    design = models.ForeignKey('designs.Design', on_delete=models.CASCADE, related_name='designed_personalizable_zone')

    dx = models.FloatField(null=True)
    dy = models.FloatField(null=True)
    dh = models.FloatField(null=True)
    dw = models.FloatField(null=True)

    class Meta:
        db_table = 'DesignedPersonalizableZones'

    def __str__(self):
        return self.personalizable_zone.name + " - " + str(self.id)

########################################################
#            Designed variant preview                  #
########################################################
class DesignedPersonalizableVariantPreview(TimeStampedModel):
    """
    A designed personalizable variant preview is linked to a designed personalizable variant, it has:
    - an id
    - a designed personalizable variant
    - image path
    multiple previews can belong to the same designed personalizable variant
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    designed_personalizable_variant = models.ForeignKey(DesignedPersonalizableVariant, on_delete=models.CASCADE, related_name='designed_personalizable_variant_preview')
    image_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'DesignedPersonalizableVariantPreviews'
    def __str__(self):
        return str(self.designed_personalizable_variant.id) + " - " + str(self.id)


########################################
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
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    personalization_method = models.ForeignKey(PersonalizationMethod, on_delete=models.CASCADE)
    self_made = models.BooleanField(default=False)

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    designed_personalizable_variant = models.ForeignKey(DesignedPersonalizableVariant, on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'Products'
        
    def __str__(self):
        return self.name + ' - ' + str(self.id)
    
    @classmethod
    def get_highest_selling_products_light(cls,offset=0, 
                                               limit=10, 
                                               categories_ids: list[str]=None,
                                               personalization_type_ids: list[str]=None):
        """
        This method should return the following information about the highest selling products:
        - full product object linked to the highest selling products (based on the order item table)
        - full category object linked to the corresponding products objects
        - full designed personalizable variant object linked to the corresponding products objects
        - full designed personalizable variant preview objects linked to the designed personalizable variant objects
        - full designed personalizable zone objects linked to the designed personalizable variant objects
        - full design objects linked to the designed personalizable zone objects
        """
        # Retrieve the highest selling products based on the order item table
        highest_selling_products = cls.objects.annotate(total_sales=Count('orderitem')).order_by('-total_sales')[offset:limit]

        # Prepare the response
        response = []

        for product in highest_selling_products:
            # Retrieve the related objects
            category = product.category
            designed_personalizable_variant = product.designed_personalizable_variant
            designed_personalizable_variant_previews = designed_personalizable_variant.designedpersonalizablevariantpreview_set.all()
            designed_personalizable_zones = designed_personalizable_variant.designed_personalizable_zone.all()
            designs = [zone.design for zone in designed_personalizable_zones]

            # Build the product information
            product_info = {
                'product': model_to_dict(product),
                'category': model_to_dict(category),
                'designed_personalizable_variant': model_to_dict(designed_personalizable_variant),
                'designed_personalizable_variant_previews': [model_to_dict(designed_personalizable_variant_preview) for designed_personalizable_variant_preview in designed_personalizable_variant_previews],
                'designed_personalizable_zones': [designed_personalizable_zones],
                'designs': designs
            }

            response.append(product_info)

        return response

    
    def get_stores_names_and_full_profiles(self):
        """
        This method should return the name and full profile of the store or the stores that the designs used in this product belong to, this can be obtained through the personalizable zones that are related to the designed personalizable 
        """
        pass
