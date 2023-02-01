from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Item, Size, SizeItemCount, ItemImage
from ..serializers.item_serializers import ItemSerializer, ItemCreateSerializer, ItemUpdateSerializer
from ..serializers.size_serializers import SizeCountSerializer
from ..serializers.item_image_serializers import CreateItemImageSerializer


class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return Item.objects.prefetch_related('images', 'sizes_count', 'sizes_count__size').select_related(
            'category').all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ItemUpdateSerializer
        elif self.action == 'create':
            return ItemCreateSerializer
        elif self.action == 'change_size_count':
            return SizeCountSerializer
        elif self.action == 'add_photo':
            return CreateItemImageSerializer
        return ItemSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data)

        if serializer.is_valid():
            item = serializer.save()
            return Response(ItemSerializer(item).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            item = serializer.save()
            if isinstance(item, Response):
                return item
            return Response(ItemSerializer(item).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def change_size_count(self, request, pk):
        data = request.data
        if not isinstance(data, list):
            return Response({"detail": "data should be a list instance"}, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=True, methods=['post'])
    def add_photo(self, request, pk):
        images = request.data.getlist('image')
        images_data = [{'image': image} for image in images]

        serializer = self.get_serializer(data=images_data, many=True)
        if serializer.is_valid():
            item = self.get_object()
            images_obj_list = [ItemImage(image=image, item=item) for image in images]
            ItemImage.objects.bulk_create(images_obj_list)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
