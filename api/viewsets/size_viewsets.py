from rest_framework import viewsets

from ..models import Size
from ..serializers.size_serializers import SizeSerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()

    def get_serializer_class(self):
        return SizeSerializer
