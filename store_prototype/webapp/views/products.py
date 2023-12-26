from django.utils.html import urlencode
from http import HTTPStatus

from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductForm, SearchForm
from webapp.models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product/index.html"
    context_object_name = "products"
    paginate_by = 3

    # paginate_orphans = 1

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["form"] = self.form
        if self.search_value:
            context["query"] = urlencode({'search': self.search_value})
            context["search_value"] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(title__icontains=self.search_value)
        queryset = queryset.order_by("category__title", "title")
        return queryset


class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = "product/product_create.html"

    # def render_to_response(self, context, **response_kwargs):
    #     response = super().render_to_response(context, **response_kwargs)
    #     if context["form"].errors:
    #         response.status_code = HTTPStatus.BAD_REQUEST
    #     return response

    def form_invalid(self, form):
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_update.html"


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product/product_delete.html"
    success_url = reverse_lazy("webapp:index")


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "product/product_view.html"
