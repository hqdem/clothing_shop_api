from django.db.models import prefetch_related_objects
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from ..models import Order, OrderItem, SIZE_CHOICES, Item, Size, ORDER_STATUS_CHOICES


class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source='item.id')
    name = serializers.CharField(source='item.name', read_only=True)
    size = serializers.CharField(max_length=10)

    class Meta:
        model = OrderItem
        fields = [
            'item_id',
            'name',
            'size',
            'item_count'
        ]

    def validate_size(self, value):
        size_choices = [size[0] for size in SIZE_CHOICES]
        if value not in size_choices:
            raise serializers.ValidationError(f'{value} is incorrect size')
        return value


class OrderItemCreateSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    size = serializers.CharField(max_length=10)
    item_count = serializers.IntegerField()

    def validate_size(self, value):
        size_choices = [size[0] for size in SIZE_CHOICES]
        if value not in size_choices:
            raise serializers.ValidationError(f'{value} is incorrect size')
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='order_items')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user_email',
            'user_contacts',
            'order_status',
            'payment_id',
            'payment_url',
            'total_price',
            'items'
        ]

    def get_total_price(self, obj):
        total_price = 0
        for order_item in obj.order_items.all():
            item = order_item.item
            price = item.sale_price if item.sale_price else item.price
            total_price += price * order_item.item_count
        return total_price


class OrderSizeSerializer(serializers.Serializer):
    order_status = serializers.CharField(max_length=10)

    def validate_order_status(self, value):
        order_status_choices = [order_status_info[0] for order_status_info in ORDER_STATUS_CHOICES]
        if value not in order_status_choices:
            raise ValidationError(f'{value} is incorrect order status')
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'user_email',
            'user_contacts',
            'items'
        ]

    def create(self, validated_data):
        items_info = validated_data.pop('items')

        item_ids = [item_info['item_id'] for item_info in items_info]
        item_sizes = [item_info['size'] for item_info in items_info]

        items = Item.objects.filter(id__in=item_ids)
        sizes = Size.objects.filter(size__in=item_sizes)

        if len(items) != len(set(item_ids)):
            prefetch_related_objects(items)
            return Response({'detail': 'One of the items has wrong id'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user_email=validated_data['user_email'],
                                     user_contacts=validated_data['user_contacts'])

        order_obj_list = []
        for item_info in items_info:
            for item in items:
                for size in sizes:
                    if item_info['size'] == size.size and item_info['item_id'] == item.id:
                        order_obj_list.append(
                            OrderItem(order=order, item=item, size=size, item_count=item_info['item_count']))
        OrderItem.objects.bulk_create(order_obj_list)

        prefetch_related_objects([order], 'order_items__item')  # for not duplicating select items

        return order
