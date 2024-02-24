# Django and Python imports
from django.db import models
from uuid import uuid4

# Models
from accounts.models import TimeStampedModel
from accounts.models import Account

class Organization(TimeStampedModel):
    """
    Every organization has a official name and a description
    """
    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)


class OrganizationMembership(TimeStampedModel):
    """
    This is a many to many relationship between organization and account
    Each membership has the following information:
    - Membership id
    - Organization id
    - Account id
    - Membership status
    - Membership role
    """
    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=100)
    def __str__(self):
        return self.organization.name + " " + self.account.username
    class Meta:
        unique_together = ['organization', 'account']

class OrganizationProfile(TimeStampedModel):
    """
    Every organization has a profile, which contains the following information:
    - Organization id
    - Organization name
    - Organization description
    - Organization logo
    - Organization address
    - Organization phone number
    - Organization email
    - Organization website
    - Organization social media links
    - Organization created at
    - Organization updated at
    """
    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False, db_index=True)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="organization_logos/")
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    social_media_links = models.JSONField()
    is_sponsored = models.BooleanField(default=False)
    def __str__(self):
        return self.organization.name


class Workshop(TimeStampedModel):
    """
    Every organization can have multiple workshops, which contains the following information:
    - Workshop id
    - Workshop name
    - Workshop description
    - Workshop location
    """
    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.TextField()
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class Inventory(TimeStampedModel):
    """
    Every workshop can have multiple inventories, which contains the following information:
    - Inventory id
    - Inventory name
    - Inventory description
    - Inventory location
    """
    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False, db_index=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.TextField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class InventoryItem(TimeStampedModel):
    """
    Every inventory can have multiple items, which contains the following information:
    - Item id
    - Item name
    - Item description
    - Item quantity
    - Item price
    - Item location
    """
    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False, db_index=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    alert_threshold = models.IntegerField(default=10)

    def __str__(self):
        return self.name
    
