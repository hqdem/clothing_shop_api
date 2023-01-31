from rest_framework import serializers

from ..models import Item
from ..serializers.size_serializers import SizeItemCountSerializer
from ..serializers.category_serializers import CategorySerializer
from ..serializers.item_image_serializers import ItemImageSerializer


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sizes = SizeItemCountSerializer(many=True, source='sizes_count')
    item_images = ItemImageSerializer(many=True, source='images')

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'category',
            'description',
            'price',
            'sale_price',
            'sizes',
            'item_images'
        ]
