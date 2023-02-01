from rest_framework import serializers

from ..models import Size, SizeItemCount


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            'id',
            'size'
        ]


class SizeCountSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField()

    class Meta:
        model = Size
        fields = [
            'size',
            'item_count'
        ]


class SizeItemCountSerializer(serializers.ModelSerializer):
    size = serializers.CharField(max_length=10)

    class Meta:
        model = SizeItemCount
        fields = [
            'size',
            'item_count'
        ]
