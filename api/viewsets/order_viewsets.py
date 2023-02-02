from rest_framework import viewsets

from ..models import Order
from ..serializers.order_serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Order.objects.prefetch_related('order_items__item', 'order_items__size').all()

    def get_serializer_class(self):
        return OrderSerializer
