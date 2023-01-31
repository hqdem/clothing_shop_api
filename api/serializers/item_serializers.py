from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response

from ..models import Item, Category, Size, SizeItemCount
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


class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=True)
    sizes = SizeItemCountSerializer(many=True, source='sizes_count')

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

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        category_id = validated_data.get('category_id', None)
        if category_id is not None:
            category = Category.objects.get_or_create(id=category_id)
        else:
            category = instance.category

        description = validated_data.get('description', instance.description)
        sizes = validated_data.get('sizes_count', None)

        # print(validated_data)
        # print(sizes)

        if sizes is not None:
            serializer = SizeItemCountSerializer(data=sizes, many=True)
            if serializer.is_valid():

                item_size_count = instance.sizes_count

                for size_count in sizes:
                    now_item_size_count = item_size_count.select_related('size', 'item').get(size__size=size_count['size']['size'])
                    now_item_size_count.item_count = size_count['item_count']
                    now_item_size_count.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance.name = name
        instance.category = category
        instance.description = description

        instance.save()

        return instance

    def create(self, validated_data):
        sizes_count = validated_data.pop('sizes_count')
        category = get_object_or_404(Category, id=validated_data['category_id'])
        item = Item.objects.create(category=category, **validated_data)
        for size in sizes_count:
            item_size = get_object_or_404(Size, size=size['size']['size'])
            SizeItemCount.objects.create(item=item, size=item_size, item_count=size['item_count'])

        return item
