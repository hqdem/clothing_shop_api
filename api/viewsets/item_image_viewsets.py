from rest_framework import viewsets

from ..models import ItemImage
from ..serializers.item_image_serializers import ItemImageSerializer


class ItemImageViewSet(viewsets.ModelViewSet):
    queryset = ItemImage.objects.all()

    def get_serializer_class(self):
        return ItemImageSerializer