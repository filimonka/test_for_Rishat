from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.dateformat import format

User = get_user_model()


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'usd'),
        ('EUR', 'eur')
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
        return f'{self.name}, {self.get_price_show()}, {self.currency}'

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

    def __str__(self):
        return f'Заказ №{self.id}'

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


class Discount(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    percentage = models.FloatField(
        verbose_name='размер скидки',
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100)
        ]
        )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='discount'
    )
    redeem_by = models.DateField(
        verbose_name='срок действия',
        blank=True,
        null=True,
    )

    def get_redeem(self):
        return format(self.redeem_by, 'U')
    
    def __str__(self):
        return f'{self.name}, {self.percentage}'


class Tax(models.Model):
    name = models.CharField(
        verbose_name='название налога',
        max_length=150,
    )
    inclusive = models.BooleanField(
        verbose_name='размер налога включен в стоимость',
        default=False
    )
    percentage = models.FloatField(
        verbose_name='размер налога',
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100)
        ]
    )
