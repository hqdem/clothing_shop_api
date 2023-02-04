from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Order
from ..serializers.order_serializers import OrderSerializer, OrderCreateSerializer, OrderSizeSerializer
from ..external.yookassa_client import create_payment, find_payment


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin):
    def get_queryset(self):
        return Order.objects.prefetch_related('order_items__item', 'order_items__size').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update_status':
            return OrderSizeSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            item = serializer.save()
            if isinstance(item, Response):
                return item

            total_price = 0
            for order_item in item.order_items.all():
                o_item = order_item.item
                price = o_item.sale_price if o_item.sale_price else o_item.price
                total_price += price * order_item.item_count

            payment = create_payment(total_price)
            item.payment_id = payment.id
            item.payment_url = payment.confirmation.confirmation_url
            item.save()

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            order = self.get_object()
            order.order_status = serializer.validated_data['order_status']
            order.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk):
        order = self.get_object()

        payment_id = str(order.payment_id)
        payment = find_payment(payment_id)

        payment_status = payment.status

        if payment_status == 'succeeded':
            order.order_status = 'created'
            order.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if payment_status == 'canceled':
            order.order_status = 'canceled'
            order.save()
        return Response({'detail': f'Not succeeded status. Status is {payment_status}'}, status=status.HTTP_402_PAYMENT_REQUIRED)
