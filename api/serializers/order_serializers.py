from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ..models import Order, OrderItem, SIZE_CHOICES, Item, Size


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source='item.name', read_only=True)
    size = serializers.CharField(max_length=10)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'name',
            'size',
            'item_count'
        ]

    def validate_size(self, value):
        size_choices = [size[0] for size in SIZE_CHOICES]
        if value not in size_choices:
            raise serializers.ValidationError(f'{value} is incorrect size')
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='order_items')

    class Meta:
        model = Order
        fields = [
            'id',
            'user_email',
            'user_contacts',
            'order_status',
            'items'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'user_email',
            'user_contacts',
            'order_status',
            'items'
        ]

    def create(self, validated_data):
        print(validated_data)
        items = validated_data.pop('items')
        order = Order.objects.create(user_email=validated_data['user_email'],
                                     user_contacts=validated_data['user_contacts'])

        order_obj_list = []
        for item_info in items:
            item = get_object_or_404(Item, id=item_info['id'])
            size = get_object_or_404(Size, size=item_info['size'])
            order_obj_list.append(OrderItem(order=order, item=item, size=size, item_count=item_info['item_count']))

        OrderItem.objects.bulk_create(order_obj_list)
        return order
