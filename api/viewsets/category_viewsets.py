from rest_framework import viewsets

from ..models import Category
from ..serializers.item_serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer
