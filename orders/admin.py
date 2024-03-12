from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'done', 'time_create', 'time_update', 'with_product')

    def with_product(self, order: Order):
        with_products_or_not = True if ProductToOrders.objects.filter(order=order).exists() else False
        return f'Наличие зеркал в заявке {with_products_or_not}'


class ProductToOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'size_for_admin', 'done')

    def size_for_admin(self, product_to_order: ProductToOrders):
        size = product_to_order.size.size
        return f'{size}'

admin.site.register(Order, OrderAdmin)
admin.site.register(ProductToOrders, ProductToOrderAdmin)
