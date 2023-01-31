from rest_framework import routers

from .viewsets.item_viewsets import ItemViewSet

router = routers.DefaultRouter()

router.register(r'items', ItemViewSet, basename='item')
