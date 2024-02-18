from rest_framework.serializers import ValidationError
import re

"""
Field validation methods for serializers
"""
def validate_email(value):
    """
    Validate the email using regular expression
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValidationError("INVALID_EMAIL")
    return value


def custom_validate_password(value):
    """
    Validate the password using regular expressions:
    - Password should be at least 12 characters long and at most 128 characters
    - Password should not contain any spaces
    - Password should contain at least one uppercase letter and one digit and one special character
    """
    if len(value) < 12 or len(value) > 128:
        raise ValidationError("INVALID_PASSWORD")
    if " " in value:
        raise ValidationError("INVALID_PASSWORD")
    if not re.search(r"[A-Z]", value):
        raise ValidationError("INVALID_PASSWORD")
    if not re.search(r"[0-9]", value):
        raise ValidationError("INVALID_PASSWORD")
    if not re.search(r"[!@#$%^&*()_+{}|:<>?]", value):
        raise ValidationError("INVALID_PASSWORD")
    return value

def validate_username(value):
    """
    Validate the username, it should not contain any special characters or digits
    should not be empty or more than 50 characters
    """
    if not value:
        if len(value) > 50 or len(value) == 0:
            raise ValidationError("INVALID_USERNAME")
        if not re.match(r"^[a-zA-Z_]*$", value):
            raise ValidationError("INVALID_USERNAME")
    return value

def validate_gender(value):
    """
    Age should be either male or female or not specified
    """
    if not value:
        if value not in ["MALE","FEMALE","NOT_SPECIFIED"]:
            raise ValidationError("INVALID_GENDER")
    return value

def validate_phone_number(value):
    """
    Validate the phone number, must be at least 10 digits long and no more than 15 digits
    """
    if not value:
        if len(value) < 10 or len(value) > 15:
            raise ValidationError("INVALID_PHONE_NUMBER")
        if not re.match(r"^[0-9]*$", value):
            raise ValidationError("INVALID_PHONE_NUMBER")
    return value

def validate_age(value):
    """
    Validate the age, it should be between 0 and 150
    """
    if not value:
        if value < 0 or value > 100:
            raise ValidationError("INVALID_AGE")
    return value

def validate_date_of_birth(value):
    """
    Validate the date of birth, it should be in the format DD-MM-YYYY, between 1900 and 2021
    """
    if not value:
        if not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19[0-9][0-9]|20[01][0-9])$", value):
            raise ValidationError("INVALID_DATE_OF_BIRTH")
    return value
