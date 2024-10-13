from django.db import models

# Create your models here.


# Create the generic abstract donation model
class Donation(models.Model):
    """
    Abstract donation model, contains:
    - title
    - description
    - longitude
    - latitude
    - category_id
    - condition
    - needs_reparation
    - anonymous_donation
    - donation_status

    """
    # Define the condition choices
    NEW = 'New'
    REFURBISHED = 'Refurbished'
    GOOD = 'Good'
    FAIR = 'Fair'
    POOR = 'Poor'
    DAMAGED = 'Damaged'
    FOR_PARTS = 'For_Parts'

    CONDITION_CHOICES = [
        (NEW, 'New'),
        (REFURBISHED, 'Refurbished'),
        (GOOD, 'Good'),
        (FAIR, 'Fair'),
        (POOR, 'Poor'),
        (DAMAGED, 'Damaged'),
        (FOR_PARTS, 'For_Parts')
    ]

    # Define the donation status choices
    AVAILABLE = 'Available'
    PENDING = 'Pending'
    CLAIMED = 'Claimed'
    DONATED = 'Donated'
    EXPIRED = 'Expired'

    DONATION_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (PENDING, 'Pending'),
        (CLAIMED, 'Claimed'),
        (DONATED, 'Donated'),
        (EXPIRED, 'Expired')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    category_id = models.CharField(max_length=36)
    condition = models.CharField(max_length=255, choices=CONDITION_CHOICES)
    needs_reparation = models.BooleanField(default=False)
    anonymous_donation = models.BooleanField(default=False)
    donation_status = models.CharField(max_length=255, choices=DONATION_STATUS_CHOICES)
    expiration_date = models.CharField(max_length=255)
    user_profile_id = models.CharField(max_length=36)

    class Meta:
        abstract = True


# Creae the abstract request model
class Request(models.Model):
    """
    Abstract request model, contains:
    - title
    - description
    - longitude
    - latitude
    - category_id
    - condition
    - needs_reparation
    - anonymous_donation
    - donation_status

    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    category_id = models.CharField(max_length=36)
    condition = models.CharField(max_length=255)
    needs_reparation = models.BooleanField(default=False)
    anonymous_request = models.BooleanField(default=False)
    request_status = models.CharField(max_length=255)
    expiration_date = models.CharField(max_length=255)
    user_profile_id = models.CharField(max_length=36)

    class Meta:
        abstract = True


# Create the UserDonation model
class UserDonation(Donation):
    """
    User donation model contains:
    - user_donation_id
    - donation_images
    - user_profile_id

    table name is user_donations
    """
    user_donation_id = models.CharField(max_length=36, primary_key=True)
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='user_donations')
    user_donation_images = models.ManyToManyField('UserDonationImage', related_name='user_donation')

    def __str__(self):
        return self.title