from django.shortcuts import render, get_object_or_404

from orders.forms import OrderForm, order_form_create
from orders.models import ProductToOrders
from products.models import *
from django.http import HttpResponse
from pages.views import info_for_page

import math


# Create your views here.

def goods(request, sort_pk=None):
    form = order_form_create(request)
    sort_name = 'сначала популярные'
    data = [{
        "product": i,
        "cost": math.ceil(float(Product.product_manager.cost(product=i))),
        "image": ImageToProduct.objects.get(product=i.id, firstPhoto=True)
    } for i in Product.objects.filter(is_published=True)]
    if sort_pk == 1:
        data = sorted(data, key=lambda item: int(item['cost']))
        sort_name = 'сначала дешевые'
    elif sort_pk == 2:
        data = sorted(data, key=lambda item: int(item['cost']), reverse=True)
        sort_name = 'сначала дорогие'
    context = {
        'sort_name': sort_name,
        'info_for_page': info_for_page,
        'basket':
            {
                f'product {product}': {
                    'name': Product.objects.get(id=product['id']).name,
                    'product': Product.objects.get(id=product['id']),
                    'id_of_many': product['id_of_many'],
                    'image': ImageToProduct.objects.get(product=product['id'], firstPhoto=True).image,
                    'cost': math.ceil(
                        float(
                            Product.product_manager.cost(
                                product=Product.objects.get(id=product['id']),
                                size=Product.product_manager.all_size(
                                    product=Product.objects.get(
                                        id=product['id']
                                    ))[product['size']] if isinstance(product['size'], int) else None
                            )
                        )
                    )
                }
                for product in request.session.get('basket')
            } if request.session.get('basket') else {},
        'form': form
    }

    return render(request, 'products/goods.html', {'mirror': data, 'context': context})


def mirror_page(request, slug_id, size_id=None):
    mirror = get_object_or_404(Product, slug=slug_id)
    context = {
        'mirror': {
            'product': mirror,
            'slag': mirror.slug,
            'cost': math.ceil(float(Product.product_manager.cost(
                product=mirror,
                size=None if size_id is None else Product.product_manager.all_size(product=mirror)[size_id]
            ))),
            'images': ImageToProduct.objects.filter(product=mirror),
            'size': Product.product_manager.minimal_size(product=mirror) if size_id is None else
            Product.product_manager.all_size(product=mirror)[size_id],
            'size_id': size_id if size_id else 0,
            'other_size': [size.size for size in Product.product_manager.all_size(product=mirror)],
            'back_light': (
                TypeBacklight.objects.get(id=BacklightToProduct.objects.get(product=mirror.id).typeBackLight.id).name if
                BacklightToProduct.objects.filter(product=mirror.id).exists() else "нет"
            ).lower(),
            'basis': 'дерево' if PlywoodBasisToProduct.objects.filter(
                product=mirror.id).exists() else "алюминевый профиль"
        },
        'basket':
            {
                f'product {product}': {
                    'name': Product.objects.get(id=product['id']).name,
                    'product': Product.objects.get(id=product['id']),
                    'id_of_many': product['id_of_many'],
                    'image': ImageToProduct.objects.get(product=product['id'], firstPhoto=True).image,
                    'cost': math.ceil(
                        float(
                            Product.product_manager.cost(
                                product=Product.objects.get(id=product['id']),
                                size=Product.product_manager.all_size(
                                    product=Product.objects.get(
                                        id=product['id']
                                    ))[product['size']] if isinstance(product['size'], int) else None
                            )
                        )
                    )
                }
                for product in request.session.get('basket')
            } if request.session.get('basket') else {},
        'info_for_page': info_for_page,
        'for_header': False
    }

    return render(request, 'products/product_page.html', {'context': context})



