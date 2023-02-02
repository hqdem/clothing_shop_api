from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.response import Response

from ..models import Order
from ..serializers.order_serializers import OrderSerializer, OrderCreateSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin):
    def get_queryset(self):
        return Order.objects.prefetch_related('order_items__item', 'order_items__size').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            item = serializer.save()
            if isinstance(item, Response):
                return item
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
