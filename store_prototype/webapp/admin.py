from django.contrib import admin

from webapp.models import Category, Product, Order, OrderProduct

admin.site.register(Category)
admin.site.register(Product)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    fields = ("product", "qty")
    readonly_fields = ("product", "qty")
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]


admin.site.register(Order, OrderAdmin)
