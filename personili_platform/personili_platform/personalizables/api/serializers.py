
# Rest framework imports
from rest_framework import serializers

# Local imports
from personalizables.models import Category, Personalizable, PersonalizableVariant, PersonalizationType, PersonalizationMethod


#################################
#                               #
#   Category up serializer      #
#                               #
#################################
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category
    """

    class Meta:
        model = Category
        fields = '__all__'


#################################
#                               #
#     PersonalizableVariant     #
#          serializer           #
#                               #
#################################
class PersonalizableVariantGetSerializer(serializers.ModelSerializer):
    """
    Serializer for PersonalizableVariant
    """

    class Meta:
        model = PersonalizableVariant
        fields = '__all__'


#################################
#                               #
#   Personalizable serializer   #
#                               #
#################################
class PersonalizableGetSerializer(serializers.ModelSerializer):
    """
    Serializer for Personalizable
    """

    class Meta:
        model = Personalizable
        fields = '__all__'


###################################
#                                 #
# PersonalizationType serializer  #
#                                 #
###################################
class PersonalizationTypeGetSerializer(serializers.ModelSerializer):
    """
    Serializer for PersonalizationType
    """

    class Meta:
        model = PersonalizationType
        fields = '__all__'

###################################
#                                 #
# PersonalizationMethod serializer#
#                                 #
###################################
class PersonalizationMethodGetSerializer(serializers.ModelSerializer):
    """
    Serializer for PersonalizationMethod
    """

    class Meta:
        model = PersonalizationMethod
        fields = '__all__'