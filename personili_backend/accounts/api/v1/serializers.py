# validators
from django.contrib.auth.password_validation import validate_password
from utils.validators import validate_age, validate_email, custom_validate_password, validate_username, validate_phone_number, validate_date_of_birth, validate_gender

# Rest Framework imports
from rest_framework import serializers

# Django imports
from django.contrib.auth import get_user_model

# Local imports
from accounts.models import AccountProfile, DeliveryAddress, PaymentMethod, Feedback, Wallet, Transaction

# get the user model
Account = get_user_model()


######################################
#                                    #
#   Main Account sign up serializer  #
#                                    #
######################################

class MainAccountSignUpserializer(serializers.Serializer):
    """
    Serializer for main account sign Up
    """

    # Fields to create the account
    password = serializers.CharField(write_only=True, 
                                     style={'input_type': 'password'},
                                     required=True,
                                     validators=[custom_validate_password, validate_password])
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True, validators=[validate_email])

    # Fields to create the account profile
    first_name = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_username])
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_username])
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True,validators=[validate_phone_number])
    date_of_birth = serializers.CharField(required=False, allow_null=True, allow_blank=True, validators=[validate_date_of_birth])
    age = serializers.CharField(required=False, allow_null=True, allow_blank=True, validators=[validate_age])
    gender = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[validate_gender])

    def validate(self, data):
        # Check that the two password entries match
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("PASSWORDS_DO_NOT_MATCH")
        return data

    def create(self, validated_data):
        # First create the account
        # Remove the password_confirm field. we don't need it anymore
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        account = Account(
            email=validated_data.get('email'),
        )
        account.set_password(password)
        account.save()

        # Second create the account the profile
        account_profile = AccountProfile(
            account=account,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            age=validated_data.get('age'),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get("gender")
        )
        account_profile.save()

        return account, account_profile


######################################
#                                    #
#   Main Account sign up serializer  #
#                                    #
######################################
class MainAccountSignInserializer(serializers.Serializer):
    """
    Serializer for main account sign in
    """
    email = serializers.EmailField(required=True, validators=[validate_email])
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Verify that both the mail and the password are not empty, and that no other fields are included
        """
        if len(data) > 2:
            raise serializers.ValidationError("INVALID_FIELDS")
        return data

#############################################
#                                           #
#   Main Account Social sign up serializer  #
#                                           #
#############################################

#################################
#                               #
#   User sign in serializer     #
#                               #
#################################

class UserSignInSerializer(serializers.ModelSerializer):
    """
    Serializer for User Sign In
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'password')
        read_only_fields = ('id', 'username', 'active', 'staff', 'superuser')


#################################
#                               #
# Delivery address serializers  #
#                               #
#################################
# Serializer for GET requests
class DeliveryAddressGetSerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery Address
    """

    # Mark all fields as required

    class Meta:
        model = DeliveryAddress
        exclude = ('created_at', 'updated_at')


# Serializer for POST requests
class DeliveryAddressCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery Address
    """
    # Mark all fields as required
    street = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    zip_code = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    class Meta:
        model = DeliveryAddress
        exclude = ('created_at', 'updated_at')
        read_only_fields = ('id', 'user_profile')


# Serializer for PUT requests
class DeliveryAddressUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery Address
    """
    class Meta:
        model = DeliveryAddress
        exclude = ('created_at', 'updated_at', 'user_profile')
        read_only_fields = ('id',)


# Serializer for DELETE requests
class DeliveryAddressDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery Address
    """
    class Meta:
        model = DeliveryAddress
        fields = ('id',)
        read_only_fields = ('id',)


class BaseDeliveryAddressSerializer(serializers.ModelSerializer):
    pass


#################################
#                               #
#  Payment Method serializer    #
#                               #
#################################

class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment Method
    """
    payment_method_name = serializers.CharField(required=True)
    cardholder_name = serializers.CharField(required=True)
    card_number = serializers.CharField(required=True)
    expiration_date = serializers.CharField(required=True)
    security_code = serializers.CharField(required=True)

    class Meta:
        model = PaymentMethod
        fields = '__all__'
        read_only_fields = ('id',)


#################################
#                               #
#       Wallet serializer       #
#                               #
#################################
class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for Wallet, all fields are required
    """
    wallet_balance = serializers.FloatField(required=True)
    wallet_currency = serializers.CharField(required=True)
    wallet_status = serializers.CharField(read_only=True)
    ccp_number = serializers.CharField(required=True)
    ccp_key = serializers.CharField(required=True)
    rip_number = serializers.CharField(required=True)

    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ('id', 'wallet_status', 'wallet_balance')


#################################
#                               #
#  Transaction serializer       #
#                               #
#################################
class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction
    """
    transaction_amount = serializers.FloatField(required=True)
    transaction_date = serializers.DateTimeField(required=True)
    transaction_type = serializers.CharField(required=True)
    transaction_status = serializers.CharField(read_only=True)
    transaction_proof = serializers.ImageField(required=True)
    transaction_proof_path = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('transaction_amount', 'transaction_date', 'transaction_type', 'transaction_status', 'transaction_proof', 'transaction_proof_path')


#################################
#                               #
#       Profile serializer      #
#                               #
#################################

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for User Profile
    """

    class Meta:
        model = AccountProfile
        exclude = ('user', 'created_at', 'updated_at')
        read_only_fields = ('id',)


#################################
#                               #
#       Feedback serializer     #
#                               #
#################################
class FeedbackCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Feedback
    """

    class Meta:
        model = Feedback
        fields = ('email', 'subject', 'message')
        read_only_fields = ('id',)
        required_fields = ('email', 'subject', 'message')
