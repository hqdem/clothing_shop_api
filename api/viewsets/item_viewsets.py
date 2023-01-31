from rest_framework import viewsets

from ..models import Item
from ..serializers.item_serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Item.objects.prefetch_related('images', 'sizes_count', 'sizes_count__size').select_related('category').all()

    def get_serializer_class(self):
        return ItemSerializer
