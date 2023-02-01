from django.db import models


SIZE_CHOICES = (
    ('one_size', 'one_size'),
    ('xl', 'xl'),
    ('l', 'l'),
    ('m', 'm'),
    ('s', 's'),
    ('xs', 'xs')
)


class Category(models.Model):
    name = models.CharField(max_length=127, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Size(models.Model):
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, verbose_name='Размер')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.size


class SizeItemCount(models.Model):
    size = models.ForeignKey('Size', on_delete=models.PROTECT, related_name='items_count', verbose_name='Размер')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='sizes_count', verbose_name='Вещь')
    item_count = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Количество вещи с размером'
        verbose_name_plural = 'Количество вещи с размером'

    def __str__(self):
        return str(self.item_count)


class ItemImage(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='images', verbose_name='Вещь')
    image = models.ImageField(blank=True, null=True, upload_to='item_images/%Y/%m/%d/', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Иллюстрация вещи'
        verbose_name_plural = 'Иллюстрации вещей'

    def __str__(self):
        return self.image.name


class Item(models.Model):
    name = models.CharField(max_length=127, verbose_name='Наименование вещи')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='items', verbose_name='Категория')
    description = models.TextField(blank=True, null=True, verbose_name='Описание вещи')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Цена со скидкой')
    sizes = models.ManyToManyField('Size', through='SizeItemCount')

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.PROTECT, related_name='orders', verbose_name='Вещь')
    order = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='order_items', verbose_name='Заказ')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, verbose_name='Размер')
    item_count = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Вещь в заказе'
        verbose_name_plural = 'Вещи в заказе'

    # def __str__(self):
    #     return self.user_email


class Order(models.Model):
    user_email = models.EmailField(verbose_name='Email пользователя')
    user_contacts = models.CharField(max_length=127, verbose_name='Контакты пользователя')
    items = models.ManyToManyField('Item', through='OrderItem')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.user_email
