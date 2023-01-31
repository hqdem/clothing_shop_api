from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Item, Size, SizeItemCount
from ..serializers.item_serializers import ItemSerializer, ItemCreateUpdateSerializer
from ..serializers.size_serializers import SizeItemCountSerializer, SizeCountSerializer


class ItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Item.objects.prefetch_related('images', 'sizes_count', 'sizes_count__size').select_related(
            'category').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ItemCreateUpdateSerializer
        elif self.action == 'change_size_count':
            return SizeCountSerializer
        return ItemSerializer

    @action(detail=True, methods=['post'])
    def change_size_count(self, request, pk):
        data = request.data

        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid():
            item = self.get_object()
            for size_data in data:
                size = get_object_or_404(Size, size=size_data['size'])
                size_count, _ = SizeItemCount.objects.get_or_create(item=item, size=size, defaults={'item_count': 0})
                size_count.item_count = size_data['item_count']
                size_count.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
