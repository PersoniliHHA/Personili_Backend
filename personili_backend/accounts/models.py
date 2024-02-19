from typing import Set
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from uuid import uuid4


class CustomUserManager(BaseUserManager):
    """Custom user manager model that implements: create_user, create_superuser and create_staff_user"""

    def create_user(self, email, password, **extra_fields):
        # creates, saves and returns a `User` with email, and password
        if not email:
            raise ValueError('Email must be set for user')

        account = self.model(email=self.normalize_email(email), **extra_fields)
        account.set_password(password)
        account.save(using=self._db)  # using=self._db is required for supporting multiple databases with Django

        return account

    def create_superuser(self, email, password, **extra_fields):
        # creates, saves and returns a `User` with email, and password
        if not email:
            raise ValueError('Email must be set for superuser')

        account = self.model(email=self.normalize_email(email), **extra_fields)
        account.set_password(password)
        account.is_admin = True
        account.is_staff = True
        account.is_superuser = True
        account.save(using=self._db)
        return account

    def create_staff_user(self, email, password, **extra_fields):
        # creates, saves and returns a `User` with email, and password
        if not email:
            raise ValueError('Email must be set for staff user')

        account = self.model(email=self.normalize_email(email), **extra_fields)
        account.set_password(password)
        account.is_staff = True
        account.save(using=self._db)
        return account


###################################
#         TimeStamped Model       #
###################################
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


#########################################
#             Account model             #
#########################################
class Account(AbstractBaseUser, TimeStampedModel):
    """Custom user model that implements:
      id primary key, email, username, active, staff, admin, created_at, updated_at"""

    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False)
    email = models.EmailField(unique=True,
                              verbose_name='email',
                              max_length=255,
                              error_messages={"unique": "A user with that email already exists."})
    
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email and password are required by default

    class Meta:
        db_table = 'account'

    def has_perm(self, perm, obj=None):
        return self.is_admin and self.is_active
    
    def has_module_perms(self, app_label):
        return self.is_admin and self.is_active
    
    def __str__(self) -> str:
        return str(self.id) + " - " + self.email 
    

#########################################
#           Account Profile model       #
#########################################

class AccountProfile(TimeStampedModel):
    """Account profile model, each account has one and only one profile.
       A blank profile is created when the account is created.
       The account profile has :
       - Account Profile id as a primary key
       - Account id as a foreign key
       - Account profile picture
       - Delivery address id as a foreign key

    """
    STATUS_CHOICES = [
        ('male', 'Male'),
        ('female', 'Published'),
        ('not specified', 'Not Specified'),
    ]


    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False, db_index=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile', db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    profile_picture_path = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'account_profile'

    def __str__(self):
        return str(self.id) + " - " + self.first_name + " " + self.last_name

    def get_phone_number(self) -> str:
        return self.phone_number

    def get_profile_picture(self) -> str:
        return self.profile_picture_path

#########################################
#             Role model                #
#########################################
class Role(TimeStampedModel):
    """
    Every role has a name and a description
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'role'

    def __str__(self) -> str:
        return self.name
    

#########################################
#          Delivery address model       #
#########################################
class DeliveryAddress(TimeStampedModel):
    """
    Delivery address model, each user has one and only one delivery address.
    The delivery address is linked to the profile table.
    A single delivery address is composed of the following fields:
    - Delivery address id as a primary key
    - Street
    - City
    - Zip code
    - State
    - Country
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, related_name='deliveryaddress')
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    zip_code = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'delivery_address'

    def __str__(self):
        return str(self.id) + " - " + self.user_profile.user.email


#########################################
#            Payment Details model      #
#########################################
class PaymentMethod(TimeStampedModel):
    """
    Payment details model, each user can have multiple payment methods. These payment methods are linked
    to one and only one user profile.
    A single payment method is composed of the following fields:
    - Payment details id as a primary key
    - User profile id as a foreign key
    - Payment method name
    - Cardholder name
    - Card number
    - Expiration date
    - Security code
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, related_name='payment_details', default=None)
    payment_method_name = models.CharField(max_length=255, null=True)
    cardholder_name = models.CharField(max_length=255, null=True)
    card_number = models.CharField(max_length=255, null=True)
    expiration_date = models.DateField(null=True)
    security_code = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'payment_details'

    def __str__(self) -> str:
        return str(self.user_profile.user.id) + " - " + self.user_profile.user.email + " - " + self.user_profile.user.username


#########################################
#            Wallet model               #
#########################################
class Wallet(TimeStampedModel):
    """
    Wallet model, each user has one and only one wallet. the wallet is linked to the profile
    A single wallet is composed of the following fields:
    - id as a primary key
    - User profile id as a foreign key one to one
    - Wallet balance
    - Wallet currency
    - Wallet status
    - CCP number
    - CCP key
    - RIP number
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    REJECTED = "rejected"
    STATUS = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (REJECTED, 'Rejected'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_profile = models.OneToOneField(AccountProfile, on_delete=models.CASCADE, related_name='wallet')
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wallet_currency = models.CharField(max_length=255, null=True)
    wallet_status = models.CharField(choices=STATUS, default=INACTIVE, max_length=255)
    ccp_number = models.CharField(max_length=255, null=True)
    ccp_key = models.CharField(max_length=255, null=True)
    rip_number = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'wallet'

    def __str__(self) -> str:
        return str(self.user_profile.user.id) + " - " + self.user_profile.user.username + ' - ' + self.user_profile.user.email


#########################################
#            Transaction model          #
#########################################
class Transaction(TimeStampedModel):
    """
    Transaction model, each wallet can have multiple transactions. These transactions are linked to one and only one wallet.
    A single transaction is composed of the following fields:
    - Transaction id as a primary key
    - Wallet id as a foreign key
    - Transaction amount
    - Transaction date
    - Transaction type
    - Transaction status
    - Transaction proof, image field
    - Transaction proof, image path
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_date = models.DateField(null=True)
    transaction_type = models.CharField(max_length=255, null=True)
    transaction_status = models.BooleanField(null=True, default=False)
    transaction_proof = models.ImageField(upload_to='transaction_proofs', blank=True)
    transaction_proof_path = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'transaction'

    def __str__(self) -> str:
        return str(self.wallet.user_profile.user.id) + ' - ' + self.wallet.user_profile.user.username + ' - ' + self.wallet.user_profile.user.email


#########################################
#            Feedback model             #
#########################################
class Feedback(TimeStampedModel):
    """
    Feedback model, unauthenticated users can send feedbacks.
    These feedbacks have email, subject, message.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=255, null=True)
    message = models.TextField(null=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self) -> str:
        return self.email + ' - ' + self.subject


#########################################
#            Blacklist model            #
#########################################
class AccountBlacklist(TimeStampedModel):
    """
    Blacklist contains an email, a reason and a date of blacklisting.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(null=True)
    ip_address = models.GenericIPAddressField(null=True)
    reason = models.TextField(null=True)
    suspended = models.BooleanField(default=True)
    banned = models.BooleanField(default=False)
    start_date_blacklisted = models.DateTimeField(null=True)
    end_date_blacklisted = models.DateTimeField(null=True)


    class Meta:
        db_table = 'blacklist_account'

    def __str__(self) -> str:
        return self.email + ' - ' + self.reason
