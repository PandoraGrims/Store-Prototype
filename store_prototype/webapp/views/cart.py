from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, TemplateView

from webapp.forms import CartForm, OrderForm
from webapp.models import Cart, Product, Order, OrderProduct


class CartAddView(PermissionRequiredMixin, View):
    model = Cart
    form_class = CartForm
    permission_required = "webapp.add_product"

    def form_invalid(self, form):
        return HttpResponseBadRequest(f"некорректное количество товара")

    def post(self, request, *args, **kwargs):

        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        qty = int(request.POST.get("qty"))

        cart = self.request.session.get("cart", {})
        if str(product.pk) in cart:
            full_qty = qty + cart[str(product.pk)]
        else:
            full_qty = qty

        if full_qty > product.amount:
            return HttpResponseBadRequest(f"Количество товара {product.title} всего {product.amount} штук")
        else:
            if str(product.pk) in cart:
                cart[str(product.pk)] += qty
            else:
                cart[str(product.pk)] = qty

        self.request.session["cart"] = cart
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("webapp:index")


class CartView(TemplateView):
    template_name = "cart/cart_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = self.request.session.get("cart", {})
        print(cart)

        total = 0
        products = []
        for product_pk, qty in cart.items():
            product = get_object_or_404(Product, pk=product_pk)
            product_total = product.price * qty
            total += product_total
            products.append({
                "product": product,
                "qty": qty,
                "product_total": product_total
            })

        context = super().get_context_data(object_list=None, **kwargs)
        context['total'] = total
        context['products'] = products
        context['form'] = OrderForm(cart=cart)
        return context


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart')


class CartDeleteOneView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart')

    def delete(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, pk=kwargs['pk'])
        success_url = self.get_success_url()

        if cart_item.qty > 1:
            cart_item.qty -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return HttpResponseRedirect(success_url)


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("webapp:index")

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        cart = self.request.session.get("cart", {})
        kwargs['cart'] = cart
        return kwargs

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors['__all__'])

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        order = form.save()

        products = []
        order_products = []
        cart = self.request.session.get("cart", {})
        print(cart)
        for product_id, qty in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            order_products.append(OrderProduct(order=order, product=product, qty=qty))
            product.amount -= qty
            products.append(product)

        OrderProduct.objects.bulk_create(order_products)
        Product.objects.bulk_update(products, ('amount',))
        self.request.session.pop("cart")
        return HttpResponseRedirect(self.success_url)


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'user_orders.html', {'orders': orders})
