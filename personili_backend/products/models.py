from django.db import models
from uuid import uuid4
from django.db.models import Q, Avg
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from accounts.models import TimeStampedModel
from accounts.models import AccountProfile
from organizations.models import Organization, Workshop
from personalizables.models import Personalizable, PersonalizableVariant, Category, Department, PersonalizationMethod, DesignedPersonalizableVariant
from designs.models import Design

from django.db.models import Count
from django.forms.models import model_to_dict



#########################################
#            Products models            #
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
    
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='workshop', null=True)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=True)

    # if not null then this means the product is self made by a user
    user = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, related_name='user', null=True)
    # self made or not, if true this mean the product was created by a regular user
    self_made = models.BooleanField(default=False)

    # to be published or not (products are created but not published until the organization decides to publish them)
    to_be_published = models.BooleanField(default=False)
    latest_publication_date = models.DateTimeField(null=True, blank=True)

    personalization_method = models.ForeignKey(PersonalizationMethod, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    # editable : this means the user can personalize the product, maybe will be replaces by templates
    editable = models.BooleanField(default=True)
    is_sponsored = models.BooleanField(default=False)

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)

    tags = models.TextField(max_length=1000, null=True, blank=True)
    
    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.title + ' - ' + str(self.id)
    
    @property
    def default_variant(self):
        return self.productvariants.first()

    @classmethod
    def get_products(   cls,  
                        offset: int,
                        limit: int,
                        
                        max_price: float=None,
                        min_price: float=None,

                        option_value_ids: list[str]=None,
                        brands: list[str]=None,
                        models: list[str]=None,

                        category_ids: list[str]=None,
                        department_ids: list[str]=None,
                        organization_ids: list[str]=None,
                        workshop_ids :list[str]=None,
                        
                        personalization_method_ids: list[str]=None,
                        design_ids: list[str]=None,
                        theme_ids: list[str]=None,
                        
                        sponsored_organizations =None,
                        sponsored_workshops=None,
                        sponsored_products=None,
                        search_term: str=None,
                        
                        publication_date: str=None,):
        
        """
        This method returns a list of products ordered by the number of sales with the following infos :
        - product id
        - product name
        - product description
        - category id
        - workshop and organization which created the designs
        - all the product variants and their reviews, designs, themes
        
        filters used :
        - category
        - organization
        - workshop
        - personalization type
        - theme of the designs used
        - title and description of the product
        """
        # Start with the base query (only non self made products) and their previews
        products = cls.objects.filter(self_made=False, to_be_published=True)
        count = products.count()
        
        # Filter the price, if at least one variant's price meets the criteria the product and its variants are returned
        if max_price and min_price:
            products =  products.filter(
                    Q(productvariants__price__lte=max_price) &
                    Q(productvariants__price__gte=min_price)
                )
            
        # Category and department filters
        if category_ids:
            # First get the leaf categories
            leaf_categories = Category.get_leaf_categories_from_list(category_ids)
            products = products.filter(category_id__in=leaf_categories)
        if department_ids:
            products = products.filter(department_id__in=department_ids)

        # Option value, brands, models filters
        if option_value_ids:
            products = products.filter(productvariants__designed_personalizable_variant__personalizable_variant__variant_values__option_value_id__in=option_value_ids)
        if brands:
            products = products.filter(productvariants__designed_personalizable_variant__personalizable_variant__personalizable_brand__in=brands)
        if models:
            products = products.filter(productvariants__designed_personalizable_variant__personalizable_variant__personalizable_model__in=models)
        
        # Organization and workshop filters
        if organization_ids:
            products = (products.filter(workshop__organization_id__in=organization_ids))
        if workshop_ids:
            products = (products.filter(workshop_id__in=workshop_ids))

        # Personalization method, theme and design filters
        #if personalization_method_ids:
        #    products = (products.filter(personalization_method_id__in=personalization_method_ids)
        #                .select_related('personalization_method'))
        
        if theme_ids:
            products = (products.filter(productvariants__designed_personalizable_variant__designed_personalizable_variant_zone__related_designs__design__theme_id__in=theme_ids))
        if design_ids:
            products = (products.filter(productvariants__designed_personalizable_variant__designed_personalizable_variant_zone__related_designs__design_id__in=design_ids))
        
        # Sponsored organizations filter
        if sponsored_organizations:
            products = (products.filter(workshop__organization__orgprofile__is_sponsored=True))
        # Sponsored workshops filter
        if sponsored_workshops:
            products = (products.filter(workshop__is_sponsored=True))
        # Sponsored products filter
        if sponsored_products:
            products = products.filter(is_sponsored=True)

        if publication_date:
            products = products.filter(latest_publication_date__gte=publication_date)
        
        # Search term filter : search in the product title and description, the product variant title and description, the organization name
        if search_term:
            products = products.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(productvariants__name__icontains=search_term) |
                Q(productvariants__description__icontains=search_term) |
                Q(workshop__organization__business_name__icontains=search_term) |
                Q(workshop__organization__orgprofile__description__icontains=search_term) |
                Q(tags__icontains=search_term) |
                Q(productvariants__designed_personalizable_variant__personalizable_variant__variant_values__option_value__option__name__icontains=search_term) |
                Q(productvariants__designed_personalizable_variant__personalizable_variant__variant_values__option_value__value__icontains=search_term) |
                Q(productvariants__designed_personalizable_variant__personalizable_variant__personalizable_brand__icontains=search_term) |
                Q(productvariants__designed_personalizable_variant__personalizable_variant__personalizable_model__icontains=search_term) 
            )   
        
        # Now get the products, their variants and their reviews, the organization info, the category, the department, the personalization method, the designs and the themes
        products = (products.select_related( 'workshop__organization', 'category', 'department')
                    .prefetch_related('productvariants__productvariantpreviews', 'productvariants__designed_personalizable_variant__personalizable_variant__variant_values__option_value__option')
                    .annotate(num_reviews=Count('productvariants__productvariantreviews'))
                    .annotate(avg_rating=Avg('productvariants__productvariantreviews__rating'))
                    .annotate(num_sales=Count('productvariants__orderitem'))
                    .order_by('-num_sales','-num_reviews', '-avg_rating')[offset:limit])
        
        
        # Now prepare the json response
        response = {"products_list": []}
        for product in products:
            product_data = {
                "product_id": product.id,
                "product_title": product.title,
                "product_description": product.description,
                "product_rating": product.avg_rating,
                "product_nb_reviews": product.num_reviews,
                "product_nb_sales": product.num_sales,
                
                "product_category_id": product.category.id,
                "product_category_name": product.category.name,
                "product_department_id": product.department.id,
                "product_department_name": product.department.name,
                
                "product_organization_id": product.workshop.organization.id,
                "product_organization_name": product.workshop.organization.business_name,
                "product_workshop_id": product.workshop.id if product.workshop else None,
                "product_workshop_name": product.workshop.name if product.workshop else None,
                
                "product_variants": [{  "product_variant_id": variant.id,
                                        "product_variant_name": variant.name,
                                        "product_variant_price": variant.price,
                                        "product_variant_quantity": variant.quantity,
                                        "product_variant_sku": variant.sku,
                                        "product_variant_values":[
                                            {
                                                "option_id": variant_value.option_value.option.id,
                                                "option_name": variant_value.option_value.option.name,
                                                "option_value_id": variant_value.option_value.id,
                                                "option_value": variant_value.option_value.value
                                            } for variant_value in variant.designed_personalizable_variant.personalizable_variant.variant_values.all()
                                        ] ,
                                        "product_variant_previews": [preview.image_path for preview in variant.productvariantpreviews.all()],
                                        } for variant in product.productvariants.all()],
                
                  }
            # Remove the null key values
            product_data = {k: v for k, v in product_data.items() if v is not None}
            
            response["products_list"].append(product_data)
        
        # Add the count of the products
        response["count"] = count

        return response


    @classmethod
    def get_full_product_details(cls, product_id: str):
        """
        This method takes a product id and returns the full details of the product:
        - Product id
        - Product title
        - Product description
        - Product variants ids, names, descriptions, prices, quantities, skus, reviews, previews, promotions
        - Product category, departement id
        - Product organization and workshop name
        - Product previews ids and images
        - Product designs ids and images
        - Product themes
        """
        product_details = (cls.objects.filter(id=product_id, self_made=False, to_be_published=True)
                              .select_related('workshop__organization__orgprofile', 'category', 'department')
                              .prefetch_related('productvariants__productvariantpreviews', 'productvariants__productvariantreviews', 'productvariants__designed_personalizable_variant__designed_personalizable_variant_zones__related_designs__design__theme')      
                              .annotate(num_reviews=Count('productvariants__productvariantreviews'))
                              .annotate(avg_rating=Avg('productvariants__productvariantreviews__rating'))
                              .annotate(num_sales=Count('productvariants__orderitem'))
                              .first())
        response: dict = {
            "product_id": product_details.id,
            "product_title": product_details.title,
            "product_description": product_details.description,
            
            "product_category_id": product_details.category.id,
            "product_category_name": product_details.category.name,
            "product_department_id": product_details.department.id,
            "product_department_name": product_details.department.name,
            
            "product_organization_id": product_details.workshop.organization.id,
            "product_organization_name": product_details.workshop.organization.business_name,
            "product_organization_logo": product_details.workshop.organization.orgprofile.logo_path,
            "product_organization_sponsored": product_details.workshop.organization.orgprofile.is_sponsored,
            "product_workshop_id": product_details.workshop.id,
            "product_workshop_name": product_details.workshop.name, 
            "product_variants": [
                {"product_variant_id": variant.id,
                    "product_variant_name": variant.name,
                    "product_variant_description": variant.description,
                    "product_variant_price": variant.price,
                    "product_variant_quantity": variant.quantity,
                    "product_variant_sku": variant.sku,
                    "product_variant_values":[
                        {
                            "option_id": variant_value.option_value.option.id,
                            "option_name": variant_value.option_value.option.name,
                            "option_value_id": variant_value.option_value.id,
                            "option_value": variant_value.option_value.value
                        } for variant_value in variant.designed_personalizable_variant.personalizable_variant.variant_values.all()
                    ] ,
                    "product_variant_previews": [preview.image_path for preview in variant.productvariantpreviews.all()],
                    } for variant in product_details.productvariants.all()],
            
            "designs_used": [{
                            "design_id": related_design.design.id,
                            "design_title": related_design.design.title,
                            "design_image_path": related_design.design.image_path,
                            "theme_id": related_design.design.theme.id,
                            "theme_name": related_design.design.theme.name,
                            "num_likes": related_design.design.design_likes.count()
                        } for product_variant in product_details.productvariants.all()
                          for zone in product_variant.designed_personalizable_variant.designed_personalizable_variant_zones.all()
                          for related_design in zone.related_designs.all()],
            
            #"product_personalization_method_id": product_details.personalization_method.id if product_details.personalization_method else None,
            #"product_personalization_method_name": product_details.personalization_method.name if product_details.personalization_method else None,
            #"product_personalization_type_id": product_details.personalization_method.personalization_type.id if product_details.personalization_method else None,
            #"product_personalization_type_name": product_details.personalization_method.personalization_type.name if product_details.personalization_method else None,
            
            "product_variants_reviews": [
                {"account_id": review.account.id,  
                 "account_username": review.account.profile.username,
                 "rating": review.rating, 
                 "comment": review.comment} for review in product_details.productvariants.productvariantreviews.all()],
            
            "product_num_reviews": product_details.num_reviews,
            "product_avg_rating": product_details.avg_rating,
            "product_num_sales": product_details.num_sales,    
            }
        return response
    
    def get_minimum_price(self):
        """
        This method returns the minimum price of the product
        """
        return self.productvariants.aggregate(models.Min('price'))['price__min']
    
class ProductVariant(TimeStampedModel):
    """
    Each product has one or more variants
    Each product variant is linked to a single designed personalizable variant
    A product variant has the following fields :
    - id
    - designed_personalizable_variant (foreign key)
    - name 
    - description
    - price
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productvariants')
    designed_personalizable_variant = models.OneToOneField(DesignedPersonalizableVariant, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0) 
    # the workshop owner can set the quantity of the product variant
    # the workshop owner receives a notification when the quantity of the product variant is low, also provide tools for them to automate the process of restocking
    sku = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'product_variants'


    def __str__(self):
        return self.product.title + " " + self.name + " " + str(self.id)
    
class ProductVariantPreview(TimeStampedModel):
    """
    This table is used to store the product preview
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='productvariantpreviews')
    image_path = models.CharField(max_length=255)

    class Meta:
        db_table = 'product_variant_previews'

    def __str__(self):
        return self.product.title + " " + str(self.id)


class ProductVariantReview(TimeStampedModel):
    """
    This table is used to store the product reviews
    the fields are : 
    - product variant
    - account
    - rating
    - comment
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='productvariantreviews')
    account_profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=1000)

    class Meta:
        db_table = 'product_reviews'

    def __str__(self):
        return self.product.title + " " + self.account.email + " " + str(self.rating) + " " + str(self.id)
    

#####################################################################################
#                             Promotions and Events                                #
#####################################################################################
class Promotion(TimeStampedModel):
    """
    Abstract class for all the promotions
    """
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    promotion_identification_code = models.CharField(max_length=255, null=True, blank=True)
    redeem_codes = models.JSONField(null=True, blank=True)
    class Meta:
        abstract = True

class DiscountPromotion(Promotion):
    """
    This is for percentage based discounts
    """
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE, null=True, blank=True)
    personalizable_variant = models.ForeignKey(PersonalizableVariant, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'discount_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id + " " + self.percentage

class AmountPromotion(Promotion):
    """
    This is for amount based discounts
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'amount_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id + " " + self.amount

class FirstTimePurchasePromotion(Promotion):
    """
    This is for first time purchase discounts
    """
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = 'first_time_purchase_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id

class LoyaltyPromotion(Promotion):
    """
    This is for loyalty discounts
    """
    points_per_purchase = models.IntegerField()
    class Meta:
        db_table = 'loyalty_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id

class ReferralPromotion(Promotion):
    """
    This is for referral discounts
    """
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        db_table = 'referral_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id
    
class FreeShippingPromotion(Promotion):
    """
    This is for free shipping discounts
    """
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = 'free_shipping_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id

class FlashSalePromotion(Promotion):
    """
    This is for flash sale discounts
    """
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        db_table = 'flash_sale_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id
    
class MembersOnlyPromotion(Promotion):
    """
    This is for members only discounts
    """
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        db_table = 'members_only_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id

class BulkPurchasePromotion(Promotion):
    """
    This is for bulk purchase discounts
    """
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        db_table = 'bulk_purchase_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id

class Event(TimeStampedModel):
    """
    This table is used to store the events
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'events'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id



