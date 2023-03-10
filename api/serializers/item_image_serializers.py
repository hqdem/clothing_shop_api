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


class CreateItemImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ItemImage
        fields = [
            'image'
        ]
