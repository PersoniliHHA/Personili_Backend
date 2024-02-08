# Rest framework imports
from rest_framework import serializers

# Local imports
from designs.models import Design, Collection, Store, Theme


#################################
#                               #
#      Designs serializer       #
#                               #
#################################
class DesignSerializerBase(serializers.ModelSerializer):
    """
    Get serializer for Design class
    """

    class Meta:
        model = Design
        exclude = ('created_at', 'updated_at')


class DesignPostSerializer(serializers.ModelSerializer):
    """
    Post serializer for Design class
    required attributes are : collection id, theme id, title, description, image file
    """
    theme = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    collection = serializers.CharField(required=False)
    tags = serializers.CharField(required=False)

    class Meta:
        model = Design
        exclude = ('created_at', 'updated_at', 'id', 'status')
        read_only_fields = ('created_at', 'updated_at', 'id', 'status', 'theme', 'collection')


class DesignGetSerializerLight(serializers.Serializer):
    """
    Get serializer for Design class
    """
    image = serializers.ImageField(required=True)
    design_title = serializers.CharField(required=True)
    store_name = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'


class DesignGetSerializerHeavy(serializers.ModelSerializer):
    pass


#################################
#                               #
#      Collection serializer    #
#                               #
#################################

class CollectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Collection, a collection is a group of designs
    The serializer should return the collection along with the designs linked to it
    This is a nested serializer with nested designs
    """

    designs = DesignSerializerBase(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ('id', 'store')

    def to_representation(self, instance):
        """
        Overriding to_representation to add the designs
        """
        response = super().to_representation(instance)
        response['designs'] = DesignSerializerBase(instance.designs.all(), many=True).data
        return response


#################################
#                               #
#      Store serializer         #
#                               #
#################################
class StoreGetSerializerLight(serializers.ModelSerializer):
    """
    Serializer for Store
    """

    class Meta:
        model = Store
        fields = '__all__'


class StoreGetSerializerHeavy(serializers.ModelSerializer):
    """
    Serializer for Store
    """

    class Meta:
        model = Store
        fields = '__all__'


class StoreSerializerPost(serializers.ModelSerializer):
    """
    Serializer for Store
    """

    class Meta:
        model = Store
        fields = ('id', 'name', 'description', 'logo', 'banner', 'theme', 'is_active', 'is_featured', 'is_verified', 'is_suspended')
