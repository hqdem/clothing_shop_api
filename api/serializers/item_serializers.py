from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ..models import Item, Category, Size, SizeItemCount, SIZE_CHOICES
from ..serializers.size_serializers import SizeCountSerializer
from ..serializers.category_serializers import CategorySerializer
from ..serializers.item_image_serializers import ItemImageSerializer


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sizes = SizeCountSerializer(many=True, source='sizes_count')
    item_images = ItemImageSerializer(many=True, source='images')
    is_available = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'category',
            'description',
            'price',
            'sale_price',
            'is_available',
            'sizes',
            'item_images'
        ]

    def get_is_available(self, obj):
        if not obj.sum_count:
            return False
        return True


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

        size_names = [size_info['size'] for size_info in sizes_count]
        sizes = Size.objects.filter(size__in=size_names)

        sizes_count_list = []
        for size in sizes:
            for size_count in sizes_count:
                if size_count['size'] == size.size:
                    sizes_count_list.append((size, size_count['item_count']))

        size_item_count_obj_list = []
        for size_to_count in sizes_count_list:
            size_item_count_obj_list.append(SizeItemCount(item=item, size=size_to_count[0], item_count=size_to_count[1]))
        SizeItemCount.objects.bulk_create(size_item_count_obj_list)

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


class ItemProcessCartSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField()
    count = serializers.IntegerField(required=True)
    size = serializers.CharField(max_length=10)

    class Meta:
        model = Item
        fields = [
            'item_id',
            'size',
            'count',
            'price'
        ]

    def validate_size(self, value):
        size_choices = [size[0] for size in SIZE_CHOICES]
        if value not in size_choices:
            raise serializers.ValidationError(f'{value} is incorrect size')
        return value
