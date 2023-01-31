from rest_framework import serializers

from ..models import Size, SizeItemCount, Item


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            'id',
            'size'
        ]


class SizeItemCountSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True)

    class Meta:
        model = Item.sizes.through
        fields = [
            'id',
            'size',
            'item_count'
        ]
