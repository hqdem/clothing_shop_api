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
    size = SizeSerializer()

    class Meta:
        model = Item.sizes.through
        fields = [
            'id',
            'size',
            'item_count'
        ]


class SizeCountSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField()

    class Meta:
        model = Size
        fields = [
            'size',
            'item_count'
        ]
