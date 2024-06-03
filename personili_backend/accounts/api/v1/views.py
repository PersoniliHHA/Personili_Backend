# Standard imports
from datetime import timezone

# rest framework imports
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



# Django imports
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction, IntegrityError, DatabaseError, Error

# Serializer imports
from accounts.api.v1.serializers import MainAccountSignUpserializer, MainAccountSignInserializer, UserProfileSerializer, WalletSerializer, TransactionSerializer, FeedbackCreateSerializer
from accounts.api.v1.serializers import DeliveryAddressCreateSerializer, DeliveryAddressUpdateSerializer, DeliveryAddressDeleteSerializer, DeliveryAddressGetSerializer, BaseDeliveryAddressSerializer
from security.permissions.is_authenticated import IsAuthenticatedWithJWT

# Models
from accounts.models import AccountProfile, ActionToken, DeliveryAddress, Wallet, Transaction, Feedback, AccountBlacklist

# drf spectacular imports
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiTypes

# Services 
from accounts.api.v1.services.email_activation import send_email_activation_link, verify_email_verification_token, verify_account_email

# Validators
from utils.validators import validate_email

# Standard imports
import logging as logger
from typing import Optional

# Security
from security.jwt import create_access_token, create_refresh_token

logger.basicConfig(level=logger.DEBUG)

Account = get_user_model()


#################################
#                               #
#     User Sign-Up ViewSet      #
#                               #
#################################

class AccountAuthViewSet(viewsets.ViewSet):
    """Viewset for the User Sign Up API"""

    queryset = Account.objects.all()
    serializer_class = MainAccountSignUpserializer

    ######################################################################################
    ###################### Main Acount APIS (login, signup, verify email, reset password)#
    ######################################################################################
    # Main account sign up api
    @action(detail=False, methods=["POST"], url_path="v1/accounts/sign-up", permission_classes=[permissions.IsAuthenticated])
    @extend_schema(
        summary="Sign up a new user",
        description="This method is used to create a new account for a user, it creates a blank account profile in the process as well.",
        request=MainAccountSignUpserializer,
        responses={
            201: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Account created successfully",
                examples=[
                    OpenApiExample(
                        "Account created successfully",
                        value={
                            "message": "ACCOUNT_CREATED",
                            "details": {
                                "email": "burger@nomail.com",
                                "first_name": "Burger",
                                "last_name": "Nomail",
                                "phone_number": "1234567890",
                                "age": 20,
                                "gender": "Male",
                                "date_of_birth": "2000-01-01",
                                "access_token": "eyJhbGciOiAiSFM1MTIiLCAidHlwIjogIkpXVCJ9",
                                "refresh_token": "eyJNsYWltcyI6IHsiaXNzIjogInBlc",

                                       }
                            }
                       )
                    ]
                ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Bad request",
                        value={
                            "ERROR": "INIVALID_REQUEST_DATA",
                            "DETAILS": {
                                "email": [
                                    "This field is required."
                                ],
                                "password": [
                                    "This field is required."
                                ]
                            }
                        }
                    )
                ]
            ),
        }
    )
    def main_account_sign_up(self, request, *args, **kwargs):
        """
        This method is used to register a new user
        Checks to make before creating a new user:
        - Check if the user with this email already exists
        - Check if the email is blacklisted or not
        - the account will be created with a its profile empty
        """
        # specify the permission and authentication classes
        self.permission_classes = [permissions.AllowAny]
        self.authentication_classes = []

        # 1- Validate the request data
        serializer = MainAccountSignUpserializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                                "ERROR": "INIVALID_REQUEST_DATA",
                                "DETAILS": serializer.errors,
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')

        #2 - Check if the email is blacklisted
        if AccountBlacklist.objects.filter(email=email).exists():
            return Response({"ERROR": "EMAIL_BLACKLISTED"}, status=status.HTTP_400_BAD_REQUEST)

        # 3 - Check if an account with this email already exists
        if Account.objects.filter(email=email).exists():
            return Response({"ERROR": "EMAIL_ALREADY_EXISTS"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                # Create both the account and the account profile
                account, account_profile = serializer.create(serializer.validated_data)
                
                # Send activation email
                send_email_activation_link(
                    email_to_activate=account.email,
                    account_id=str(account.id),
                    first_name=account_profile.first_name,
                    last_name=account_profile.last_name
                )

                return Response({"message": "Account created, check email for account activation",}, status=status.HTTP_201_CREATED)

        except (IntegrityError, DatabaseError, Error) as e:
            return Response({"ERROR": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Main account sign in api
    @action(detail=False, methods=["POST"], url_path="v1/accounts/sign-in", permission_classes=[permissions.AllowAny])
    def main_account_sign_in(self, request, *args, **kwargs):
        """This method is used to sign in a user"""

        # specify the permission and authentication classes
        self.permission_classes = [permissions.AllowAny]
        self.authentication_classes = []

        # Validate the request data
        serializer = MainAccountSignInserializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                                "ERROR": "BAD_REQUEST",
                                "DETAILS": serializer.errors,
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Get the email and password from the serializer
        email: str = serializer.validated_data.get('email')
        password: str = serializer.validated_data.get('password')

        # Authenticate the user
        account = authenticate(email=email, password=password)
        if account is None:
            return Response({"error": "INVALID_EMAIL_OR_PASSWORD"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the account is active
        if not account.is_active:
            return Response({"error": "ACCOUNT_NOT_ACTIVATED"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if the account is suspended or banned (in the blacklist)
        blacklist_entry = AccountBlacklist.objects.filter(email=account.email).first()
        if blacklist_entry and (blacklist_entry.banned or (blacklist_entry.suspended and blacklist_entry.suspension_end_date < timezone.now())):
            return Response({"error": "ACCOUNT_SUSPENDED_OR_BANNED"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if the email is verified
        if not account.email_verified:
            return Response({"error": "EMAIL_NOT_VERIFIED"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate the access and refresh tokens
        access_token = create_access_token(str(account.id))
        refresh_token = create_refresh_token(str(account.id))

        return Response({"message": "SUCCESSFUL LOGIN",
                         "details": {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                         }},status=status.HTTP_200_OK)

    # Main account email verification api
    @action(detail=False, methods=["GET"], url_path="v1/accounts/verify-email/(?P<token>[^/.]+)", permission_classes=[permissions.AllowAny])
    def main_account_verify_email(self, request, token:str, *args, **kwargs):
        """
        This api will be used to verify the email of the user, it extracts the token from the path parameters and checks its existence and validity
        """
        print("token: ", token)
        
        # Verify the token
        is_token_valid, account_id = verify_email_verification_token(token, "EMAIL_VERIFICATION")
        if not is_token_valid:
            return Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark the user email as verified
        verify_account_email(account_id)

        return Response({"message": "EMAIL_VERIFIED"}, status=status.HTTP_200_OK)

    # Resend activation email api
    @action(detail=False, methods=["POST"], url_path="v1/accounts/resend-activation-email", permission_classes=[permissions.AllowAny])
    def main_account_resend_activation_email(self, request, *args, **kwargs):
        """
        This api will be used to resend the activation email to the user, it extracts the email from the request data
        """
        email: str = request.data.get('email')
        
        # check if the email is valid and not null
        if not email or not validate_email(email):
            return Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if an account with this email already exists
        if not Account.objects.filter(email=email).exists():
            return Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the email is blacklisted or suspended
        if AccountBlacklist.is_email_blacklisted(email):
            return Response({"error": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the email isn't already active
        if Account.objects.filter(email=email).first().email_verified:
            return Response({"error": "EMAIL_ALREADY_VERIFIED"}, status=status.HTTP_400_BAD_REQUEST)

        # Now check if there is already an action token for this email, if there delete it
        if ActionToken.objects.filter(email=email, action="EMAIL_VERIFICATION").exists():
            ActionToken.objects.filter(email=email, action="EMAIL_VERIFICATION").delete()
        else:
            return Response({"error": "UNAUTHORIZED"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the account id
        account_id = Account.objects.filter(email=email).first().id

        # Send activation email
        send_email_activation_link(
            email_to_activate=email,
            account_id=str(account_id)
        )

        return Response({"message": "ACTIVATION_EMAIL_RESENT"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["POST"], url_path="v1/main-account-update-password", permission_classes=[permissions.IsAuthenticated])
    def main_account_update_password(self, request, *args, **kwargs):
        """This method is used to update the user password"""

        return None
    
    @action(detail=False, methods=["POST"], url_path="v1/main-account-update-email", permission_classes=[permissions.IsAuthenticated])
    def main_account_update_email(self, request, *args, **kwargs):
        """This method is used to update the user email"""

        return None
    
    @action(detail=False, methods=["POST"], url_path="v1/main-account-social-sign-up", permission_classes=[permissions.AllowAny])
    def main_account_social_sign_up(self, request, *args, **kwargs):
        """This method is used to sign up a user using social media"""

        return None
    
    @action(detail=False, methods=["POST"], url_path="v1/main-account-social-sign-in", permission_classes=[permissions.AllowAny])
    def main_account_social_sign_in(self, request, *args, **kwargs):
        """This method is used to sign in a user using social media"""

        return None
    
    @action(detail=False, methods=["POST"], url_path="v1/refresh", permission_classes=[permissions.IsAuthenticated])
    def main_account_refresh(self, request, *args, **kwargs):
        """This method is used to refresh the user token"""

        return None
    
    
#################################
#                               #
#        Profile ViewSet        #
#                               #
#################################


class AccountProfileViewSet(viewsets.ModelViewSet):
    """
    Viewset for the Profile API,
    only authenticated users can access this api and only their profile
    """

    serializer_class = UserProfileSerializer
    # Set the permission, only authenticated users can access this api and only their profile
    permission_classes = [ProfileApiPermission]

#################################
#                               #
#        Feedback ViewSet       #
#                               #
#################################
class PublicFeedbackViewSet(viewsets.ModelViewSet):
    """
    Viewset for the Feedback API, all users can access this api to submit feedbacks
    """

    serializer_class = FeedbackCreateSerializer
    # Set the permission, all users can access this api
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Feedback.objects.all()

    @action(detail=True, methods=["POST"], url_path="create-new-feedback",)
    def create_new_feedback(self, request, *args, **kwargs):
        """
        Create a new feedback
        """

        # Create the serializer
        serializer = FeedbackCreateSerializer(data=request.data)

        # Check if the serializer is valid
        serializer.is_valid(raise_exception=True)

        # Save the feedback
        serializer.save()

        # Create the response
        response = Response()
        response.data = serializer.data
        response.status = status.HTTP_201_CREATED

        return response
