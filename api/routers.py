from rest_framework import routers

from .viewsets.item_viewsets import ItemViewSet
from .viewsets.category_viewsets import CategoryViewSet
from .viewsets.item_image_viewsets import ItemImageViewSet

router = routers.DefaultRouter()

router.register(r'items', ItemViewSet, basename='item')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'images', ItemImageViewSet, basename='item-image')
