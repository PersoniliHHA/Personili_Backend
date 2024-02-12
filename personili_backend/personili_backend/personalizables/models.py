# Standard libraries
from uuid import uuid4

# Django
from django.db import models

# Models
from accounts.models import TimeStampedModel
from treebeard.mp_tree import MP_Node

# Utilities
from utils.utilities import store_image_in_s3, get_presigned_url_for_image


#########################################
#             Category model            #
#########################################
class Category(TimeStampedModel, MP_Node):
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
    description = models.TextField(null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    logo_path = models.CharField(max_length=255, null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    availability_status = models.CharField(max_length=255, choices=AVAILABILITY_STATUS_CHOICES, default='Unavailable')

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
    
    def build_category_tree(self):
        """
        - This method returns a dictionary with the category tree, according to the following rules:
        - If a parent subcategory has no subcategories, then it is a leaf, only return leafs that are either available or coming soon.
        - If a non-leaf category has all subcategories who are neither available nor coming soon, then don't return it, and this includes all the subcategories in the tree line.
        - Consistency rule : if a parent category is marked as available, 
        then at least one of its subcategories must be available or coming soon. 
        If the parent category is marked by any other status othan than available 
        then all its subcategories must be marked with the same status .
        """
        if self.availability_status == 'Available' or self.availability_status == 'ComingSoon':
            if self.get_direct_subcategories():
                return {
                    'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'image_path': self.image_path,
                    'logo_path': get_presigned_url_for_image(self.logo_path),
                    'parent_category': self.parent_category.id if self.parent_category else None,
                    'availability_status': "ComingSoon" if self.parent_category and Category.objects.get(pk=self.parent_category.id).availability_status == "ComingSoon"  else self.availability_status,
                    'subcategories': [category.build_category_tree() for category in self.subcategories.all()]
                }
            else:
                return {
                    'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'image_path': self.image_path,
                    'logo_path': get_presigned_url_for_image(self.logo_path),
                    'parent_category': self.parent_category.id if self.parent_category else None,
                    'availability_status': "ComingSoon" if self.parent_category and Category.objects.get(pk=self.parent_category.id).availability_status == "ComingSoon"  else self.availability_status,
                    'subcategories': []
                }
    
    @classmethod
    def get_all_categories_and_their_subcategories(cls):
        """
        This method returns all categories and their subcategories
        It first gets the root categories, then it gets the subcategories of each root category using the build_category_tree method
        """
        root_categories = cls.objects.filter(parent_category=None)
        return [root_category.build_category_tree() for root_category in root_categories]


    
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
    an availability and linked to a subcategory
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    availability = models.BooleanField(default=True)

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
                'color': Color.objects.get(pk= variant.color.id).hex_code,
                'size': Size.objects.get(pk= variant.size.id).name,
                'material': Material.objects.get(pk = variant.material.id).code,
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
#              Colors model             #
#########################################
class Color(TimeStampedModel):
    """
    A color has an id, a name, a hex code
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    hex_code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name + " - " + self.hex_code

#########################################
#             Material model            #
#########################################
class Material(TimeStampedModel):
    """
    A material has an id, a name and a specific code
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name + " - " + self.code
    
#########################################
#                Size model             #
#########################################
class Size(TimeStampedModel):
    """
    A size has an id, a list of fixed choices and a name
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name + " - " + self.code

#########################################
#      PersonalizableVariant model      #
#########################################
class PersonalizableVariant(TimeStampedModel):
    """
    A personalizable variant is linked to one and only one printable,
    it has a color
    a size
    a material ( set of choices )
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable = models.ForeignKey(Personalizable, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='variants_of_a_color')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='variants_of_a_size')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='variants_of_a_material')
    stock_quantity = models.IntegerField(null=True)
    
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


    def __str__(self):
        return self.personalizable.name + " - " + self.name


########################################################
#  Allowed personalizable/personalization methd model  #
########################################################
class AllowedPersonalizablesPersonalization(TimeStampedModel):
    """
    Associates the id of the personalizable and the id of the allowed personalization type
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable = models.ForeignKey(Personalizable, on_delete=models.CASCADE, related_name='allowed_personalizables')
    personalization_type = models.ForeignKey(PersonalizationType, on_delete=models.CASCADE, related_name='allowed_personalization_types')

    def __str__(self):
        return self.personalizable.name + " - " + str(self.id)

########################################################
#                Designed Zone model                   #
########################################################
class DesignedPersonalizableVariant(TimeStampedModel):
    """
    A designed personalizable variant is linked to a personalizable variant 
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable_variant = models.ForeignKey(PersonalizableVariant, on_delete=models.CASCADE, related_name='designed_personalizable_variant')


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

    def __str__(self):
        return self.personalizable_zone.name + " - " + str(self.id)






