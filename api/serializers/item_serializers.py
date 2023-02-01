from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ..models import Item, Category, Size, SizeItemCount
from ..serializers.size_serializers import SizeCountSerializer
from ..serializers.category_serializers import CategorySerializer
from ..serializers.item_image_serializers import ItemImageSerializer


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sizes = SizeCountSerializer(many=True, source='sizes_count')
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


class ItemCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=True)
    sizes = SizeCountSerializer(many=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'category_id',
            'description',
            'price',
            'sale_price',
            'sizes'
        ]

    def create(self, validated_data):
        sizes_count = validated_data.pop('sizes')
        category = get_object_or_404(Category, id=validated_data['category_id'])
        item = Item.objects.create(category=category, **validated_data)

        for size in sizes_count:
            item_size = get_object_or_404(Size, size=size['size'])
            SizeItemCount.objects.create(item=item, size=item_size, item_count=size['item_count'])
        return item


class ItemUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'category_id',
            'description',
            'price',
            'sale_price',
        ]

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        category_id = validated_data.get('category_id', None)
        if category_id is not None:
            category, _ = Category.objects.get_or_create(id=category_id)
        else:
            category = instance.category

        description = validated_data.get('description', instance.description)

        instance.name = name
        instance.category = category
        instance.description = description

        instance.save()

        return instance
