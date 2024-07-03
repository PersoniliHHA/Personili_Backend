# Standard libraries
from typing import Iterable
from uuid import uuid4

# Django
from django.db import models
from django.db.models import Count
from django.forms.models import model_to_dict

# Models
from accounts.models import TimeStampedModel
from organizations.models import InventoryItem
from designs.models import Design



#######################################################
"""
Each personalizable has many options linked to it, like colors and sizes and materials
Each personalizable can have many personalizable variants:
 -- a variant is defined by a set of combinations between the option value of the personalizable and the personalizable
    This combination is called personalizable variant value
 """
#######################################################

#########################################
#             Department model          #
#########################################
class Department(TimeStampedModel):
    """
    Department model has a name, a description and a picture.
    List of departments :
    - Women 
    - Men
    - Children
    - Babies
    - Unisex
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    
    # Icons and images for each department
    image_path_1 = models.CharField(max_length=255, null=True, blank=True)
    image_path_2 = models.CharField(max_length=255, null=True, blank=True)
    image_path_3 = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return self.name + " - " + str(self.id)


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
    description = models.TextField(null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    availability_status = models.CharField(max_length=255, choices=AVAILABILITY_STATUS_CHOICES, default='Available')

    # Icons and images for each category
    image_path_1 = models.CharField(max_length=255, null=True, blank=True)
    image_path_2 = models.CharField(max_length=255, null=True, blank=True)
    image_path_3 = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'categories'

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
        This method returns the entire category tree under a specific parent category, if the parent
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
                category_dict["image_path_1"] = category.image_path_1
                category_dict["image_path_2"] = category.image_path_2
                category_dict["image_path_3"] = category.image_path_3
                category_dict["sub_categories"] = cls.get_category_tree(category.id)
                category_tree.append(category_dict)
        
        return category_tree


    @classmethod
    def get_leaf_categories_from_list(cls, 
                                      category_ids: list[str]):
        """
        This method takes a list of ids containing categories and returns a list of leaf categories, if a category has subcategories then it is not a leaf category.
        If a category in the category_ids is already a leaf category then it is added to the list of leaf categories
        """
        leaf_categories = []
        for category_id in category_ids:
            # check if the category has subcategories
            subcategories = Category.objects.filter(parent_category=category_id)
            if len(subcategories) == 0:
                leaf_categories.append(category_id)
            else:
                leaf_categories.extend(cls.get_leaf_categories_from_list([subcategory.id for subcategory in subcategories]))
        
        return leaf_categories


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
        db_table = 'options'

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
        db_table = 'option_values'

    def __str__(self):
        return self.value + " - " + str(self.option.name)

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
    image_path_1 = models.CharField(max_length=255, null=True, blank=True)
    image_path_2 = models.CharField(max_length=255, null=True, blank=True)
    image_path_3 = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'personalization_types'

    def __str__(self):
        """
        Returns the name of the personalization type
        """
        return self.name + " - " + str(self.id)
        
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
    image_path_1 = models.CharField(max_length=255, null=True, blank=True)
    image_path_2 = models.CharField(max_length=255, null=True, blank=True)
    image_path_3 = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        db_table = 'personalization_methods'

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
    A personalizable has a name, description, brand, model, category, department
    Each
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    
    brand = models.CharField(max_length=255, null=True, default="Generic Brand")
    model = models.CharField(max_length=255, null=True, default="Generic Model")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')

    # Designs that can be used on this personalizable
    allowed_designs = models.ManyToManyField(Design, related_name='personalizables')

    # Usage and design constraints
    # An open personalizable means any design can be used on it by the users
    is_open_for_personalization = models.BooleanField(default=False)

    # A personalizable can be a template, meaning that it can be used as a template for creating an editable product by designers
    can_be_template = models.BooleanField(default=False)

    # Parameters for personalizable usage with other designs
    used_with_store_designs = models.BooleanField(default=False)
    used_with_user_uploaded_designs = models.BooleanField(default=False)
    used_with_same_workshop_designs = models.BooleanField(default=False)
    used_with_other_workshop_designs = models.BooleanField(default=False)
    used_with_platform_designs = models.BooleanField(default=False)
    

    class Meta:
        db_table = 'personalizables'


    def __str__(self):
        return self.name + " - " + self.category.name + " - " + str(self.id)

    def save(self, *args, **kwargs):
        """
        This method saves the personalizable object
        """
        # Validate the usage parameters of the personalizable
        if self.is_open_for_personalization :
            self.used_with_specific_designs = False
            self.used_with_specific_workshops = False
            self.used_with_designers_designs = False
            self.userd_with_user_uploaded_designs = False
            self.used_with_platform_designs = False
        elif any([self.used_with_specific_designs, self.used_with_specific_workshops, self.used_with_designers_designs, self.userd_with_user_uploaded_designs, self.used_with_platform_designs]):
            self.is_open_for_personalization = False

        super().save()
    
#########################################
#      PersonalizableVariant model      #
#########################################
class PersonalizableVariant(TimeStampedModel):
    """
    A personalizable variant is linked to a sku in the inventory item table and to a personalizable
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    personalizable = models.ForeignKey(Personalizable, on_delete=models.CASCADE, related_name='variants')
    quantity = models.IntegerField(null=True, default=1)
    
    def __str__(self):
        return "variant of : " + self.personalizable.name + " - " + str(self.id)
    
    class Meta:
        db_table = 'personalizable_variants'

    def get_the_variant_values(self):
        """
        This method returns the option values of this personalizable variant
        """
        pass

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
        db_table = 'personalizable_options'

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
    an image path and coordinates x1, y1, x2, y2
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable = models.ForeignKey(Personalizable, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=255, null=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    max_nb_designs = models.IntegerField(null=True, default=1)
    x1 = models.FloatField(null=True)
    y1 = models.FloatField(null=True)
    x2 = models.FloatField(null=True)
    y2 = models.FloatField(null=True)

    class Meta:
        db_table = 'personalizable_zones'

    def __str__(self):
        return self.personalizable.name + " - " + self.name + " - " + str(self.id)


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
        db_table = 'personalizable_variant_values'

    def __str__(self):
        return self.personalizable_variant.personalizable.name + " - " + self.option_value.value + " - " + str(self.id)


########################################################
#                Designed variant model                #
########################################################
class DesignedPersonalizableVariant(TimeStampedModel):
    """
    A designed personalizable variant is linked to:
     - a personalizable variant 
     - a product : each product can have many designed personalizable variants, but a designed personalizable variant is linked to one and only one product
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable_variant = models.ForeignKey(PersonalizableVariant, on_delete=models.CASCADE, related_name='designed_personalizable_variant')
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'designed_personalizable_variants'

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
    designed_personalizable_variant = models.ForeignKey(DesignedPersonalizableVariant, on_delete=models.CASCADE, related_name='designed_personalizable_variant_zone')
    design = models.ForeignKey('designs.Design', on_delete=models.CASCADE, related_name='designed_personalizable_zone')


    dx1 = models.FloatField(null=True)
    dy1 = models.FloatField(null=True)
    dx2 = models.FloatField(null=True)
    dy2 = models.FloatField(null=True)

    class Meta:
        db_table = 'designed_personalizable_zones'

    def __str__(self):
        return self.personalizable_zone.name + " - " + str(self.id)
