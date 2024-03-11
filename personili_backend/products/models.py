from django.db import models
from uuid import uuid4
from django.db.models import Q, Avg
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from accounts.models import TimeStampedModel
from accounts.models import Account
from organizations.models import Organization, Workshop
from personalizables.models import Category, PersonalizationMethod

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
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='workshop', null=True)

    # if it's self made it won't be published on the store (made by the buyer himself)
    self_made = models.BooleanField(default=False)

    # to be published or not (products are created but not published until the organization decides to publish them)
    to_be_published = models.BooleanField(default=False)

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.title + ' - ' + str(self.id)

    @classmethod
    def get_products(cls,
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
        products = cls.objects.filter(self_made=False, to_be_published=True)
        
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
            products = (products.filter(product_designed_personalizable_variant__designed_personalizable_variant_zone__design__theme_id__in=theme_ids)
                        .prefetch_related('product_designed_personalizable_variant__designed_personalizable_variant_zone__design__theme'))
        if design_ids:
            products = (products.filter(product_designed_personalizable_variant__designed_personalizable_variant_zone__design_id__in=design_ids)
                        .prefetch_related('product_designed_personalizable_variant__designed_personalizable_variant_zone__design'))
        if sponsored_organizations:
            products = (products.filter(organization__orgprofile__is_sponsored=True)
                        .select_related('organization'))
        if search_term:
            products = products.filter(Q(title__icontains=search_term) | 
                                       Q(description__icontains=search_term))
        
        # Now get the products and their previews ordered by the number of sales and average rating
        products = (products.prefetch_related('productpreview', 'organization', 'category', 'product_designed_personalizable_variant__designed_personalizable_variant_zone__design__theme')
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
                "product_workshop_id": product.workshop.id if product.workshop else None,
                "product_price": product.price,
                "product_designs": [{"design_id": zone.design.id, 
                                     "theme_id": zone.design.theme.id, 
                                     "design_image_path": zone.design.image_path} for variant in product.product_designed_personalizable_variant.all() for zone in variant.designed_personalizable_variant_zone.all()],
                "product_preview": [preview.image_path for preview in product.productpreview.all()],
                "product_theme_ids": [zone.design.theme.id for variant in product.product_designed_personalizable_variant.all() for zone in variant.designed_personalizable_variant_zone.all()] if theme_ids else None,
                  }
            # Remove the null key values
            product_data = {k: v for k, v in product_data.items() if v is not None}
            
            response["products_list"].append(product_data)
        
        
        # Add the count of the products
        response["count"] = len(response["products_list"])

        return response


    @classmethod
    def get_full_product_details(cls, product_id: str):
        """
        This method takes a product id and returns the full details of the product:
        - Product id
        - Product title
        - Product description
        - Product price
        - Product category
        - Product organization and workshop name
        - Product reviews
        - Product previews ids and images
        - Product designs ids and images
        - Product themes
        """
        product_details = (cls.objects.filter(id=product_id)
                              .select_related('organization__orgprofile', 'workshop' 'category', 'personalization_method__personalization_type')
                              .prefetch_related('productpreview', 'productreview', 'product_designed_personalizable_variant__designed_personalizable_variant_zone__design__theme')      
                              .annotate(num_reviews=Count('productreview'))
                              .annotate(avg_rating=Avg('productreview__rating'))
                              .annotate(num_sales=Count('orderitem'))
                              .annotate(num_design_likes=Count('product_designed_personalizable_variant__designed_personalizable_variant_zone__design__designlike'))
                              .first())
        response: dict = {
            "product_id": product_details.id,
            "product_title": product_details.title,
            "product_description": product_details.description,
            "product_price": product_details.price,
            "product_category_id": product_details.category.id,
            "product_category_name": product_details.category.name,
            "product_organization_id": product_details.organization.id,
            "product_organization_name": product_details.organization.name,
            "product_organization_logo": product_details.organization.orgprofile.logo_path,
            "product_organization_sponsored": product_details.organization.orgprofile.is_sponsored,
            "product_workshop_id": product_details.workshop.id if product_details.workshop else None,
            "product_workshop_name": product_details.workshop.name if product_details.workshop else None,
            "product_personalization_method_id": product_details.personalization_method.id if product_details.personalization_method else None,
            "product_personalization_method_name": product_details.personalization_method.name if product_details.personalization_method else None,
            "product_personalization_type_id": product_details.personalization_method.personalization_type.id if product_details.personalization_method else None,
            "product_personalization_type_name": product_details.personalization_method.personalization_type.name if product_details.personalization_method else None,
            "product_reviews": [
                {"account_id": review.account.id, 
                 "account_email": review.account.email, 
                 "rating": review.rating, 
                 "comment": review.comment} for review in product_details.productreview.all()],
            "product_previews": [{"image_path": preview.image_path} for preview in product_details.productpreview.all()],
            "designs_used": [{"design_id": zone.design.id, 
                              "design_image_path": zone.design.image_path, 
                              "theme_id": zone.design.theme.id, 
                              "theme_name": zone.design.theme.name,
                              "design_likes": zone.design.num_design_likes 
                              } for variant in product_details.product_designed_personalizable_variant.all() for zone in variant.designed_personalizable_variant_zone.all()],
            "product_num_reviews": product_details.num_reviews,
            "product_avg_rating": product_details.avg_rating,
            "product_num_sales": product_details.num_sales,    
            }
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


class ProductReview(TimeStampedModel):
    """
    This table is used to store the product reviews
    the fields are : 
    - product
    - account
    - rating
    - comment
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

    class Meta:
        abstract = True

class DiscountPromotion(Promotion):
    """
    This is for percentage based discounts
    """
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        db_table = 'discount_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id + " " + self.percentage

class ProductDiscountPromotion(models.Model):
    """
    This is for percentage based discounts
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_promotion = models.ForeignKey(DiscountPromotion, on_delete=models.CASCADE)
    class Meta:
        db_table = 'product_discount_promotions'
        unique_together = ['product', 'discount_promotion']

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

class CodePromotion(Promotion):
    """
    This is for code based discounts
    """
    code = models.CharField(max_length=255)
    class Meta:
        db_table = 'code_promotions'

    def __str__(self):
        return self.product.title + " " + self.start_date + " " + self.end_date + " " + self.is_active + " " + self.id + " " + self.code

class FirstTimePurchasePromotion(Promotion):
    """
    This is for first time purchase discounts
    """
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
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



