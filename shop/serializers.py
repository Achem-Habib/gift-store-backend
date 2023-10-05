from rest_framework import serializers

from .models import Category, Image, Occasion, Product, RecipientType


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image',
                  'description', 'subcategories')

    def get_subcategories(self, obj):
        subcategories = Category.objects.filter(parent_category=obj)
        serializer = CategorySerializer(subcategories, many=True)
        return serializer.data


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# occassion serializer
class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = "__all__"


# recipient type serializer
class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientType
        fields = "__all__"


# Image serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    occasions = OccasionSerializer(many=True, read_only=True)
    recipient_types = RecipientSerializer(many=True, read_only=True)
    more_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
