from django.db import models
from uuid import uuid4
from django.db.models import Q, Avg
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from accounts.models import TimeStampedModel
from accounts.models import Account
from designs.models import Design, Collection, Store, Theme
from organizations.models import Organization
from personalizables.models import Category, Personalizable, PersonalizationMethod, DesignedPersonalizableVariant, DesignedPersonalizableZone

from django.db.models import Count
from django.forms.models import model_to_dict



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
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    personalization_method = models.ForeignKey(PersonalizationMethod, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    # if it's self made it won't be published on the store
    self_made = models.BooleanField(default=False)

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.title + ' - ' + str(self.id)

    @classmethod
    def get_products_light(cls,
                           offset: int,
                           limit: int,
                           max_price: float=None,
                           min_price: float=None,
                           category_ids: list[str]=None,
                           organization_ids: list[str]=None,
                           personalization_method_ids: list[str]=None,
                           design_ids: list[str]=None,
                           theme_ids: list[str]=None,
                           sponsored_organizations =None,
                           search_term: str=None):
        
        """
        This method returns a list of products ordered by the number of sales with the following infos :
        - product id
        - product name
        - product description
        - product reviews
        - product preview
        - category id
        - theme ids attached to each design used in the product
        - workshop and organization which created the designs
        
        filters used :
        - category
        - organization
        - personalization type
        - theme of the designs used
        - title and description of the product
        """
        # Start with the base query (only non self made products) and their previews
        products = cls.objects.filter(self_made=False)
        
        # Filter the price
        if max_price and min_price:
            products = products.filter(price__lte=max_price, price__gte=min_price)
        
        # Add filters incrementally
        if category_ids:
            products = products.filter(category_id__in=category_ids)
        if organization_ids:
            products = (products.filter(organization_id__in=organization_ids)
                        .select_related('organization'))
        if personalization_method_ids:
            products = (products.filter(personalization_method_id__in=personalization_method_ids)
                        .select_related('personalization_method'))
        if theme_ids:
            products = (products.filter(productdesignedpersonalizablevariant__designed_personalizable_variant__designed_personalizable_zone__design__theme_id__in=theme_ids)
                        .prefetch_related('productdesignedpersonalizablevariant__designed_personalizable_variant__designed_personalizable_zone__design__theme'))
        if design_ids:
            products = (products.filter(productdesignedpersonalizablevariant__designed_personalizable_variant__designed_personalizable_zone__design_id__in=design_ids)
                        .prefetch_related('productdesignedpersonalizablevariant__designed_personalizable_variant__designed_personalizable_zone__design'))
        if sponsored_organizations:
            products = (products.filter(organization__orgprofile__is_sponsored=True)
                        .select_related('organization'))
        if search_term:
            products = products.filter(Q(title__icontains=search_term) | 
                                       Q(description__icontains=search_term))
        
        # Now get the products and their previews ordered by the number of sales and average rating
        products = (products.prefetch_related('productpreview', 'organization', 'category')
                    .annotate(num_reviews=Count('productreview'))
                    .annotate(avg_rating=Avg('productreview__rating'))
                    .annotate(num_sales=Count('orderitem'))
                    .order_by('-num_sales','-num_reviews', '-avg_rating')[offset:offset+limit])
        
        # Now prepare the json response
        response = {"products_list": []}
        for product in products:
            product_data = {
                "product_id": product.id,
                "product_title": product.title,
                "product_description": product.description,
                "product_rating": product.avg_rating,
                "product_num_reviews": product.num_reviews,
                "product_num_sales": product.num_sales,
                "product_category_id": product.category.id,
                "product_organization_id": product.organization.id,
                "product_organization_name": product.organization.name,
                "product_price": product.price,
                "product_preview": [preview.image_path for preview in product.productpreview.all()],
                "product_theme_ids": [zone.design.theme.id for zone in product.productdesignedpersonalizablevariant.designed_personalizable_variant.designed_personalizable_zone.all()] if theme_ids else None,
                "product_designs": [zone.design.id for zone in product.productdesignedpersonalizablevariant.designed_personalizable_variant.designed_personalizable_zone.all()] if design_ids else None
            }
            # Remove the null key values
            product_data = {k: v for k, v in product_data.items() if v is not None}
            
            response["products_list"].append(product_data)
        
        
        # Add the count of the products
        response["count"] = len(response["products_list"])

        return response

                

class ProductPreview(TimeStampedModel):
    """
    This table is used to store the product preview
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productpreview')
    image_path = models.CharField(max_length=255)

    class Meta:
        db_table = 'product_previews'

    def __str__(self):
        return self.product.title + " " + self.id
    

class ProductDesignedPersonalizableVariant(TimeStampedModel):
    """
    This table is a junction table between the product and the designed personalizable variant tables
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productdesignedpersonalizablevariant')
    designed_personalizable_variant = models.ForeignKey(DesignedPersonalizableVariant, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_designed_personalizable_variants'
        unique_together = ['product', 'designed_personalizable_variant']

    def __str__(self):
        return self.product.title + " " + self.designed_personalizable_variant.name
    

class Promotion(TimeStampedModel):
    """
    Abstract class for all the promotions
    """
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class DiscountPromotion(Promotion):
    """
    This is for percentage based discounts
    """
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discountpromotion')
    class Meta:
        db_table = 'discount_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id + " " + self.percentage

class AmountPromotion(Promotion):
    """
    This is for amount based discounts
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='amountpromotion')
    class Meta:
        db_table = 'amount_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id + " " + self.amount

class CodePromotion(Promotion):
    """
    This is for code based discounts
    """
    code = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='codepromotion')
    class Meta:
        db_table = 'code_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id + " " + self.code

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


class ProductReview(TimeStampedModel):
    """
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productreview')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=1000)

    class Meta:
        db_table = 'product_reviews'

    def __str__(self):
        return self.product.title + " " + self.account.email + " " + self.rating + " " + self.id