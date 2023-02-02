from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Item, Size, SizeItemCount, ItemImage
from ..serializers.item_serializers import ItemSerializer, ItemCreateSerializer, ItemUpdateSerializer, ItemProcessCartSerializer
from ..serializers.size_serializers import SizeCountSerializer, SizeSerializer
from ..serializers.item_image_serializers import CreateItemImageSerializer


class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        queryset = Item.objects.prefetch_related('images', 'sizes_count', 'sizes_count__size').select_related(
            'category').annotate(sum_count=Sum('sizes_count__item_count')).all()
        only_available = self.request.query_params.get('available', None)
        if only_available is not None:
            return queryset.annotate(sum_count=Sum('sizes_count__item_count')).filter(sum_count__gt=0)
        return queryset

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ItemUpdateSerializer
        elif self.action == 'create':
            return ItemCreateSerializer
        elif self.action in ['change_size_count', 'get_available_sizes']:
            return SizeCountSerializer
        elif self.action == 'add_photo':
            return CreateItemImageSerializer
        elif self.action in ['check_items_availability', 'check_items_price']:
            return ItemProcessCartSerializer
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
            return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)
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

    @action(detail=True, methods=['get'])
    def get_available_sizes(self, request, pk):
        item = self.get_object()
        size = request.query_params.get('size', None)

        if size is not None:
            size_serializer = SizeSerializer(data={"size": size})
            if not size_serializer.is_valid():
                return Response(size_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            queryset = item.get_available_sizes(size=size)
        else:
            queryset = item.get_available_sizes()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def check_items_availability(self, request):
        data = request.data
        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid():
            vd = serializer.validated_data
            item_ids = [item['item_id'] for item in vd]

            items = Item.objects.filter(id__in=item_ids)
            if len(items) != len(set(item_ids)):
                return Response({'detail': 'One of product ids is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            error_items_msg = []
            for item in items:
                item_id = item.id
                for request_item in vd:
                    if item_id == request_item['item_id']:
                        try:
                            size_count = item.get_available_sizes(size=request_item['size'])[0]
                        except IndexError:
                            error_items_msg.append({'detail': f"{item.name} - {request_item['size']} isn't available"})
                            continue

                        max_count = size_count.item_count
                        if max_count < request_item['count']:
                            error_items_msg.append({'detail': f"{item.name} - {request_item['size']} isn't available. Maximum count is {max_count}"})

            if len(error_items_msg):
                return Response({'errors': error_items_msg}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def check_items_price(self, request):
        data = request.data
        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid():
            vd = serializer.validated_data
            item_ids = [item['item_id'] for item in vd]

            items = Item.objects.filter(id__in=item_ids)
            if len(items) != len(set(item_ids)):
                return Response({'detail': 'One of product ids is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            error_items_msg = []
            for item in items:
                item_id = item.id
                for request_item in vd:
                    if item_id == request_item['item_id']:
                        sale_price = item.sale_price
                        price = sale_price if sale_price else item.price
                        if price != request_item['price']:
                            error_items_msg.append({'detail': f'Incorrect price for {item.name}. Correct price is {price}'})

            if len(error_items_msg):
                return Response({'errors': error_items_msg}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
