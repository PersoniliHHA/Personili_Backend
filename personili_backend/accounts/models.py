from datetime import UTC, datetime, timedelta
from typing import Set, Tuple, List
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

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
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
        db_table = 'accounts'

    def has_perm(self, perm, obj=None):
        return self.is_admin and self.is_active
    
    def has_module_perms(self, app_label):
        return self.is_admin and self.is_active
    
    @classmethod
    def verify_email(cls, account_id: str):
        """
        Verify the email of the account
        """
        account = cls.objects.get(id=account_id)
        account.email_verified = True
        account.save()
        return account
    
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
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Published'),
        ('not specified', 'Not Specified'),
    ]


    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile', db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    profile_picture_path = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default='not specified', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    social_media_links = models.JSONField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'account_profiles'

    def __str__(self):
        return str(self.id) + " - " + self.account.email


class ActionToken(TimeStampedModel):
    """
    This model will store tokens that are used for password reset, email verification, etc.
    Each token has a type, these are the allowed types :
    - EMAIL_VERIFICATION
    - PASSWORD_RESET
    - ACCOUNT_ACTIVATION
    - ACCOUNT_SUSPENSION
    """
    EMAIL_VERIFICATION = 'email_verification'
    PASSWORD_RESET = 'password_reset'
    ACCOUNT_SUSPENSION = 'account_suspension'
    TOKEN_TYPES = [
        (EMAIL_VERIFICATION, 'EMAIL_VERIFICATION'),
        (PASSWORD_RESET, 'PASSWORD_RESET'),
        (ACCOUNT_SUSPENSION, 'ACCOUNT_SUSPENSION'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    token = models.CharField(max_length=255, unique=True)
    token_type = models.CharField(max_length=255, choices=TOKEN_TYPES, default=EMAIL_VERIFICATION)
    expiry_date = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='action_tokens')

    class Meta:
        db_table = 'action_tokens'
    
    @classmethod
    def verify_token(cls, token: str, type: str) -> Tuple[bool, str]:
        """
        This method check if the token is exists and that it's not expired and of the correct type. If it's valid
        it returns True and deletes the token, otherwise it returns False
        """
        try:
            token = cls.objects.get(token=token, token_type=type)
            if token.expiry_date > datetime.now(UTC):
                token.delete()
                return True, token.account.id
            return False, None
        except cls.DoesNotExist:
            return False, None

    def __str__(self) -> str:
        return self.token + ' - ' + self.token_type  + ' - ' + self.account.email
    
    @classmethod
    def create_new_token(cls, token:str, account_id :str, token_type: str, expiry_date: datetime) -> str:
        """
        This method creates a new token for the account and returns the token
        """
        token = cls.objects.create(
            token=token,
            account_id=account_id,
            token_type=token_type,
            expiry_date=expiry_date if expiry_date else datetime.now(UTC) + timedelta(days=1)
        )
        return token.token
        
#########################################
#             Permission model          #
#########################################
class Permission(TimeStampedModel):
    """
    Permission model, each role can have multiple permissions. These permissions are linked to one and only one role.
    A single permission is composed of the following fields:
    - Permission id as a primary key
    - Role id as a foreign key
    - Permission name
    - Permission description
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    permission_name = models.CharField(max_length=255, null=True)
    permission_description = models.TextField(null=True)

    class Meta:
        db_table = 'permissions'

    def __str__(self) -> str:
        return self.permission_name
    
#########################################
#             Role model                #
#########################################
class Role(TimeStampedModel):
    """
    Every role has a name and a description, and each role can have multiple permissions.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    class Meta:
        db_table = 'roles'

    def __str__(self) -> str:
        return self.name

#########################################
#             Role-permission model     #
#########################################
class RolePermission(TimeStampedModel):
    """
    Role-permission model, each role can have multiple permissions. These permissions are linked to one and only one role.
    A single role-permission is composed of the following fields:
    - Role permission id as a primary key
    - Role id as a foreign key
    - Permission id as a foreign key
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

    class Meta:
        db_table = 'role_permissions'

    def __str__(self) -> str:
        return self.role.name + ' - ' + self.permission.permission_name


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

    default_delivery_address = models.BooleanField(default=False)

    class Meta:
        db_table = 'delivery_addresses'

    @classmethod
    def get_delivery_addresses_by_account_profile(cls, account_profile_id: str) -> list[dict]:
        """
        This method returns a list of delivery addresses related to an account profile
        """
        delivery_addresses = cls.objects.filter(account_profile_id=account_profile_id)
        response : List[dict] = []
        for delivery_address in delivery_addresses:
            response.append({
                "id": delivery_address.id,
                "street": delivery_address.street,
                "city": delivery_address.city,
                "zip_code": delivery_address.zip_code,
                "state": delivery_address.state,
                "country": delivery_address.country,
                "default_delivery_address": delivery_address.default_delivery_address
            })

        return response

    @classmethod
    def is_owner_of_delivery_address(cls, account_profile_id: str, delivery_address_id: str) -> bool:
        """
        Check if a given account profile is the owner of a given delivery address
        """
        return cls.objects.filter(account_profile_id=account_profile_id, id=delivery_address_id).exists()
    
    def __str__(self):
        return str(self.id) + " - " + self.account_profile.account.email


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
        db_table = 'payment_methods'

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
        db_table = 'wallets'

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
        db_table = 'transactions'

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
        db_table = 'feedbacks'

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
        db_table = 'blacklist_accounts'

    @classmethod
    def is_email_blacklisted(cls, email: str) -> bool:
        """
        Check if an email is suspended or blacklisted, if it is return True
        A suspended email is an email that is temporarily banned, meaning 
        there is at least a single entry where the email is either banned or
        suspended with a end date that hasn't expired
        """
        account = cls.objects.filter(email=email)
        if account:
            for entry in account:
                if entry.suspended and entry.end_date_blacklisted > datetime.now(UTC):
                    return True
                if entry.banned:
                    return True
        return False

    @classmethod
    def is_ip_blacklisted(cls, ip_address: str) -> bool:
        """
        Check if an ip address is suspended or blacklisted, if it is return True
        A suspended ip address is an ip address that is temporarily banned, meaning 
        there is at least a single entry where the ip address is either banned or
        suspended with a end date that hasn't expired
        """
        account = cls.objects.filter(ip_address=ip_address)
        if account:
            for entry in account:
                if entry.suspended and entry.end_date_blacklisted > datetime.now(UTC):
                    return True
                if entry.banned:
                    return True
        return False
    def __str__(self) -> str:
        return self.email + ' - ' + self.reason
