from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Product, Cart, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["qty"]


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop("cart")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = ["name", "phone", "address"]

    def clean(self):
        data = super().clean()
        for product_id, qty in self.cart.items():
            product = Product.objects.get(pk=product_id)
            if qty > product.amount:
                raise ValidationError(f"Товар {product.title} закончился")
        return data
