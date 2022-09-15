from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'usd'),
        ('RUB', 'rub')
    ]
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=200,
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.IntegerField(
        verbose_name='Цена',
    )
    currency = models.CharField(
        verbose_name='валюта оплаты',
        max_length=3,
        choices=CURRENCY_CHOICES
    )

    def get_price_show(self):
        return '{0:.2f}'.format(self.price / 100)

    def __str__(self):
        return f'{self.name}, {self.get_price_show}, {self.currency}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='Покупатель'
    )
    product = models.ManyToManyField(
        Item,
        related_name='ordered',
        through='ItemInOrder',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ItemInOrder(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='order'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
    )

    def __str__(self):
        return f'{self.item.name} в заказе {self.order.id}'
