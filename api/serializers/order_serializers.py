from rest_framework import serializers

from ..models import Order, OrderItem, SIZE_CHOICES


class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source='item.id')
    item_name = serializers.CharField(source='item.name')
    size = serializers.CharField(max_length=10)

    class Meta:
        model = OrderItem
        fields = [
            'item_id',
            'item_name',
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
            'user_email',
            'user_contacts',
            'order_status',
            'items'
        ]
