# Standard libraries
from typing import Iterable
from uuid import uuid4

# Django
from django.db import models
# Django
from django.db import models
from django.db.models import Q

# Models
from accounts.models import TimeStampedModel
from organizations.models import InventoryItem
from designs.models import Design
from organizations.models import Workshop


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
    
    @classmethod
    def get_all_departments(cls):
        """
        Get all the departments
        """
        departments = Department.objects.all()
        department_list = []
        for department in departments:
            department_dict = {}
            department_dict["id"] = department.id
            department_dict["name"] = department.name
            department_dict["description"] = department.description
            department_dict["image_path_1"] = department.image_path_1
            department_dict["image_path_2"] = department.image_path_2
            department_dict["image_path_3"] = department.image_path_3
            department_list.append(department_dict)
        
        return department_list


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
        
        return option_values_list
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
    A personalizable is linked to a workshop.
    it has a name, 
    description, 
    brand, model
    category
    department

    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='personalizables')
    
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
            self.used_with_store_designs = False
            self.used_with_user_uploaded_designs = False
            self.used_with_same_workshop_designs = False
            self.used_with_other_workshop_designs = False
            self.used_with_platform_designs = False
        elif any([self.used_with_store_designs, 
                  self.used_with_user_uploaded_designs, 
                  self.used_with_same_workshop_designs, 
                  self.used_with_other_workshop_designs, 
                  self.used_with_platform_designs]):
            self.is_open_for_personalization = False

        super().save()
    
    @classmethod
    def get_personalizables(cls,
                            search_term: str = None,
                            min_price: float = None,
                            max_price: float = None,
                            model: str = None,
                            brand: str = None,
                            category_ids: str = None,
                            department_ids: str = None,
                            workshops_ids  = None,
                            organizations_ids = None,
                            promotions_ids = None,
                            option_values_ids = None,
                            sponsored_personalizables = False,
                            sponsored_organizations = False,
                            sponsored_workshops = False,
                            events_ids = None,
                            offset = 0,
                            limit = 20):
                            
        """
        Get a list of personlizables based on a set of filters.
        Filters can be :
            - search term
            - price min and max
            - model
            - brand   
            - category
            - department
            - workshops
            - organizations
            - promotions
            - option values (color, size, material)
            - sponsored personalizables
            - sponsored organizations
            - sponsored workshops
            - events
            - limit and offset
            - most popular (highest sales)
        - include all the details of each personalizable
        - include infos about the workshop and the organization
        - include all the variants and their options and options values
        - include the category and the department as well
        """
        q_objects = Q()
        # Filter only for active workshops
        q_objects.add(Q(workshop__is_active=True), Q.AND)
        if search_term:
            q_objects.add(Q(name__icontains=search_term) | 
                            Q(description__icontains=search_term) | 
                            Q(brand__icontains=search_term) | 
                            Q(model__icontains=search_term) |
                            Q(category__name__icontains=search_term) |
                            Q(department__name__icontains=search_term) |
                            Q(workshop__name__icontains=search_term) |
                            Q(workshop__description__icontains=search_term) |
                            Q(workshop__organization__name__icontains=search_term) |
                            Q(workshop__organization__description__icontains=search_term), Q.AND)

        if min_price :
            q_objects.add(Q(price__gte=min_price), Q.AND)
        if max_price :
            q_objects.add(Q(price__lte=max_price), Q.AND)
        if model:
            q_objects.add(Q(model__icontains=model), Q.AND)
        if brand:
            q_objects.add(Q(brand__icontains=brand), Q.AND)
        if category_ids:
            q_objects.add(Q(category__in=category_ids), Q.AND)
        if department_ids:
            q_objects.add(Q(department__in=department_ids), Q.AND)
        if workshops_ids:
            q_objects.add(Q(workshop__in=workshops_ids), Q.AND)
        if organizations_ids:
            q_objects.add(Q(workshop__organization__in=organizations_ids), Q.AND)
        if promotions_ids:
            q_objects.add(Q(promotions__in=promotions_ids), Q.AND)
        if option_values_ids:
            q_objects.add(Q(variants__variant_values_option_value__in=option_values_ids), Q.AND)
        if sponsored_personalizables:
            q_objects.add(Q(sponsored_personalizables=True), Q.AND)
        if sponsored_organizations:
            q_objects.add(Q(workshop__organization__orgprofile__sponsored=True), Q.AND)
        if sponsored_workshops:
            q_objects.add(Q(workshop__is_sponsored=True), Q.AND)
        
        # Add the events filter and highest sales filter later
        personalizables = (cls.objects.filter(q_objects)
                           .select_related('workshop__organization__orgprofile', 'category', 'department')
                           .prefetch_related('variants__variant_values__option_value'))[offset:limit]
        
        result = {"personalizables_list": []}
        for personalizable in personalizables:
            personalizable_dict = {}
            personalizable_dict["personalizable_id"] = personalizable.id
            personalizable_dict["personalizable_name"] = personalizable.name
            personalizable_dict["personalizable_description"] = personalizable.description
            personalizable_dict["personalizable_brand"] = personalizable.brand
            personalizable_dict["personalizable_model"] = personalizable.model
            personalizable_dict["category"] = personalizable.category.name
            personalizable_dict["department"] = personalizable.department.name
            personalizable_dict["workshop"] = personalizable.workshop.name
            personalizable_dict["workshop_description"] = personalizable.workshop.description
            personalizable_dict["organization_name"] = personalizable.workshop.organization.business_name
            personalizable_dict["organization_logo"] = personalizable.workshop.organization.orgprofile.logo_path
            personalizable_dict["organization_sponsored"] = personalizable.workshop.organization.orgprofile.is_sponsored
            personalizable_dict["variants"] = []
            for variant in personalizable.variants.all():
                variant_dict = {}
                variant_dict["id"] = variant.id
                variant_dict["name"] = variant.name
                variant_dict["quantity"] = variant.quantity
                variant_dict["variant_values"] = []
                for variant_value in variant.variant_values.all():
                    variant_value_dict = {}
                    variant_value_dict["id"] = variant_value.id
                    variant_value_dict["option_value"] = variant_value.option_value.value
                    variant_value_dict["option"] = variant_value.personalizable_option.option.name
                    variant_dict["variant_values"].append(variant_value_dict)
                personalizable_dict["variants"].append(variant_dict)
            result["personalizables_list"].append(personalizable_dict)

        
        return result




        

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
    personalizable_variant = models.ForeignKey(PersonalizableVariant, on_delete=models.CASCADE, related_name='variant_values')
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE, related_name='variant_values')
    personalizable_option = models.ForeignKey(PersonalizableOption, on_delete=models.CASCADE, related_name='variant_values')
    
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
    - it has an id and a foreign key to a personalizable zone and foreign key to the designed personalizable variant
    - a designed personalizable zone can be linked to multiple designs with many to many relationship
    and also 4 coordinates dx, dy, dh, dw
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    personalizable_zone = models.ForeignKey(PersonalizableZone, on_delete=models.CASCADE, related_name='designed_personalizable_zone')
    designed_personalizable_variant = models.ForeignKey(DesignedPersonalizableVariant, on_delete=models.CASCADE, related_name='designed_personalizable_variant_zone')
    
    # Represents the shapes, texts and other components of the design
    components = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'designed_personalizable_zones'

    def __str__(self):
        return self.personalizable_zone.name + " - " + str(self.id)

class DesignedPersonalizableZoneDesign(models.Model):
    """
    A designed personalizable zone can have many designs linked to it
    """
    designed_personalizable_zone = models.ForeignKey(DesignedPersonalizableZone, on_delete=models.CASCADE, related_name='designs')
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='designed_personalizable_zone')

    # Coordinates of the design in the zone
    dx = models.FloatField(null=True)
    dy = models.FloatField(null=True)
    dh = models.FloatField(null=True)
    dw = models.FloatField(null=True)

    class Meta:
        db_table = 'designed_personalizable_zone_designs'

