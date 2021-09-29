from rest_framework import serializers

from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        """Meta class of TagSerializer."""

        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
