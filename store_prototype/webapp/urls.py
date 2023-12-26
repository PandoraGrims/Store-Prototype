from django.urls import path

from webapp.views import ProductListView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductUpdateView, \
    CartAddView, CartView, CartDeleteView, CartDeleteOneView, OrderCreate, user_orders

app_name = "webapp"

urlpatterns = [

    path('', ProductListView.as_view(), name="index"),
    path('products/add/', ProductCreateView.as_view(), name="product_add"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name="product_delete"),
    path('product/<int:pk>/add-cart/', CartAddView.as_view(), name="product_add_cart"),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/<int:pk>/remove-one/', CartDeleteOneView.as_view(), name="delete_from_cart_one"),
    path('cart/<int:pk>/remove/', CartDeleteView.as_view(), name="delete_from_cart"),

    path('order/create/', OrderCreate.as_view(), name="order_create"),
    path('user/orders/', user_orders, name='user_orders'),
]

for urlpattern in urlpatterns:
    print(urlpattern.pattern)
