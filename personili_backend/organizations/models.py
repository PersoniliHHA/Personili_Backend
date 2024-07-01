# Django and Python imports
from django.db import models
from uuid import uuid4

# Models
from accounts.models import TimeStampedModel
from accounts.models import Account, Role, AccountProfile


class BusinessOwnerProfile(TimeStampedModel):
    """
    A business owner profile contains the following information:
    - Business owner id
    - Business owner first name
    - Business owner last name
    - Business owner full address
    - Business owner identification number
    - Account profile id
    - Business owner biography
    - Business owner contact email
    - Business owner contact phone
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    account_profile = models.OneToOneField(AccountProfile, on_delete=models.CASCADE, related_name='business_owner_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_address = models.TextField(max_length=255)
    identification_number = models.CharField(max_length=100)
    
    biography = models.TextField(null=True)
    contact_email = models.EmailField(null=True, unique=True)
    contact_phone = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'business_owner_profiles'

    def __str__(self):
        return self.full_name
    
class Organization(TimeStampedModel):
    """
    Every organization has a official name and a description
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    business_owner_profile = models.ForeignKey(BusinessOwnerProfile, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    legal_name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)

    tax_number = models.CharField(max_length=100, null=True)
    registration_number = models.CharField(max_length=100, null=True)
    registratioin_date = models.DateField(null=True)
    registration_country = models.CharField(max_length=100, null=True)
    registration_certificate_path = models.CharField(max_length=255, null=True)
    
    organization_contact_email = models.EmailField(null=True, unique=True)
    organization_contact_phone = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'organizations'

    def __str__(self):
        return self.name

class OrganizationProfile(TimeStampedModel):
    """
    Every organization has a profile, which contains the following information:
    - Organization id
    - Logo path
    - Banner path
    - Sponsored status
    - Head office address
    - Social media links

    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='orgprofile')
    logo_path = models.CharField(max_length=255, null=True, blank=True)
    banner_path = models.CharField(max_length=255, null=True, blank=True)
    is_sponsored = models.BooleanField(default=False)
    
    head_office_address = models.TextField(max_length=255)
    social_media_links = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'organization_profiles'


    def __str__(self):
        return self.organization.name


class OrganizationMembership(TimeStampedModel):
    """
    This is a many to many relationship between organization and account
    Each membership has the following information:
    - Membership id
    - Organization id
    - Account id
    - Membership status (active or inactive)
    - Membership role
    """ 
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active_membership = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['organization', 'account']
        db_table = 'organization_memberships'

    def __str__(self):
        return self.organization.name + " " + self.account.email


class Workshop(TimeStampedModel):
    """
    Every organization can have multiple workshops, which contains the following information:
    - Workshop id
    - Workshop name
    - Workshop description
    - Workshop location
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_sponsored = models.BooleanField(default=False)
    description = models.TextField(max_length=255, null=True)
    address = models.TextField(max_length=255, null=True)
    contact_email = models.EmailField(null=True, unique=True)
    contact_phone = models.CharField(max_length=25, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'workshops'

    def __str__(self):
        return self.name + " " + self.organization.name

class WorkshopMembership(TimeStampedModel):
    """
    This is a many to many relationship between workshop and account
    Each membership has the following information:
    - workshop membership id
    - workshop id
    - account id
    - organization membership id
    - membership status
    - membership role
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active_membership = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['workshop', 'account']
        db_table = 'workshop_memberships'

    def __str__(self):
        return self.workshop.name + " " + self.account.email

    
class Inventory(TimeStampedModel):
    """
    Every workshop can have multiple inventories, which contains the following information:
    - Inventory id
    - Inventory name
    - Inventory description
    - Inventory location
    - Inventory status : empty, partially filled, full
    """
    STATUS = (
        ('empty', 'Empty'),
        ('partially_filled', 'Partially Filled'),
        ('full', 'Full')
    )


    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='empty')

    class Meta:
        db_table = 'inventories'

    def __str__(self):
        return self.name
    
class InventoryItem(TimeStampedModel):
    """
    Every inventory can have multiple items, which contains the following information:
    - Item id
    - Item sku
    - Item name
    - Item description
    - Item quantity
    - Item price
    - Item location
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    sku = models.CharField(max_length=30, unique=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    alert_threshold = models.IntegerField(default=10)

    class Meta:
        db_table = 'inventory_items'

    def __str__(self):
        return self.name
    
