from rest_framework import routers

from .viewsets.item_viewsets import ItemViewSet
from .viewsets.category_viewsets import CategoryViewSet
from .viewsets.item_image_viewsets import ItemImageViewSet
from .viewsets.size_viewsets import SizeViewSet
from .viewsets.order_viewsets import OrderViewSet

router = routers.DefaultRouter()

router.register(r'items', ItemViewSet, basename='item')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'images', ItemImageViewSet, basename='item-image')
router.register(r'sizes', SizeViewSet, basename='size')
router.register(r'orders', OrderViewSet, basename='order')
