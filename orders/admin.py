from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'done', 'time_create', 'time_update')


admin.site.register(Order, OrderAdmin)
admin.site.register(ProductToOrders)
