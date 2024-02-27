from django.urls import path, include

from orders.views import add_to_basket, remove_from_basket, basket_list

app_name = 'orders'

urlpatterns = [
    path('basket/', include([
        path('', basket_list, name='list'),
        path('<int:product_id>/add/', add_to_basket, name='add'),
        path('<int:product_id>/add/<int:size_id>/', add_to_basket, name='add_with_size'),
        path('<int:product_id>/remove/', remove_from_basket, name='remove'),
    ])),
]
