from django.contrib import admin

from .models import Category, Size, ItemImage, Item, Order


class SizeItemCountInline(admin.TabularInline):
    model = Item.sizes.through


class ItemImageInline(admin.TabularInline):
    model = ItemImage


class ItemAdmin(admin.ModelAdmin):
    inlines = (SizeItemCountInline, ItemImageInline)


admin.site.register(Category)
admin.site.register(Size)
admin.site.register(ItemImage)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
