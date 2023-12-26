from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")

    def __str__(self):
        return f"{self.pk} {self.title}"

    class Meta:
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    description = models.TextField(max_length=50, null=False, blank=False, verbose_name="Описание")
    amount = models.PositiveIntegerField(verbose_name="Остаток")
    price = models.DecimalField(verbose_name="Цена", max_digits=7, decimal_places=2, validators=(MinValueValidator(0),))
    category = models.ForeignKey("webapp.Category", on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return f"{self.pk} {self.title}"

    def get_absolute_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.pk})

    class Meta:
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Cart(models.Model):
    qty = models.PositiveIntegerField(verbose_name="Количество", default=1, validators=(MinValueValidator(1),))
    product = models.ForeignKey("webapp.Product", on_delete=models.CASCADE, verbose_name="Продукт")

    def get_total_price(self):
        return self.qty * self.product.price

    @classmethod
    def get_full_total(cls):
        return cls.objects.aggregate(total=Sum(F("product__price") * F("qty")))['total']

    def __str__(self):
        return f"{self.product} {self.qty}"

    class Meta:
        verbose_name = "товар в корзине"
        verbose_name_plural = "товары в корзине"


class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    address = models.CharField(max_length=100, verbose_name="Адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    products = models.ManyToManyField('webapp.Product', related_name='orders', verbose_name='Продукты',
                                      through='webapp.OrderProduct', through_fields=('order', 'product'))
    user = models.ForeignKey(get_user_model(), models.CASCADE, blank=True,
                             null=True,
                             related_name='orders',
                             verbose_name='Пользователь')
    def __str__(self):
        return f"{self.name} {self.phone}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderProduct(models.Model):
    qty = models.PositiveIntegerField(verbose_name="Количество", validators=(MinValueValidator(1),))
    product = models.ForeignKey("webapp.Product", on_delete=models.CASCADE,
                                verbose_name="Продукт", related_name="order_products")

    order = models.ForeignKey("webapp.Order", on_delete=models.CASCADE,
                              verbose_name="Заказ", related_name="order_products")

    def __str__(self):
        return f"{self.product} {self.qty}"

    class Meta:
        verbose_name = "товар в заказе"
        verbose_name_plural = "товары в заказе"