from rest_framework import serializers

from core.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        """Meta class of TagSerializer."""

        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serialzier for ingredient objects."""

    class Meta:
        """Meta class of IngredientSerializer."""

        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
