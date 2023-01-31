from rest_framework import serializers

from ..models import ItemImage


class ItemImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(source='image')

    class Meta:
        model = ItemImage
        fields = [
            'id',
            'image_url'
        ]
