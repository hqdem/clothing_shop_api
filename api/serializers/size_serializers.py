from rest_framework import serializers

from ..models import Size


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
