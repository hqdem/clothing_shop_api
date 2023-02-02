from django.contrib import admin

from .models import Category, Size, ItemImage, Item, Order, OrderItem


class SizeItemCountInline(admin.TabularInline):
    model = Item.sizes.through


class ItemImageInline(admin.TabularInline):
    model = ItemImage


class ItemAdmin(admin.ModelAdmin):
    inlines = (SizeItemCountInline, ItemImageInline)


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)


admin.site.register(Category)
admin.site.register(Size)
admin.site.register(ItemImage)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
