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
        "cost": math.ceil(float(cost(product=i))),
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
                        'image': ImageToProduct.objects.get(product=product['id'], firstPhoto=True).image,
                        'cost': math.ceil(float(cost(product=Product.objects.get(id=product['id']))))
                    }
                for product in request.session.get('basket')
            } if request.session.get('basket') else {},
        'form': form
    }

    return render(request, 'products/goods.html', {'mirror': data, 'context': context})


def mirror_page(request, slug_id):
    mirror = get_object_or_404(Product, slug=slug_id)
    context = {
        "mirror": {
            "product": mirror,
            "cost": math.ceil(float(cost(product=mirror))),
            "images": ImageToProduct.objects.filter(product=mirror.id),
            "size": SizeToProduct.objects.get(product=mirror.id, initially=True).size,
            "back_light": (
                TypeBacklight.objects.get(id=BacklightToProduct.objects.get(product=mirror.id).typeBackLight.id).name if
                BacklightToProduct.objects.filter(product=mirror.id).exists() else "нет"
            ).lower(),
            "basis": "фанера" if PlywoodBasisToProduct.objects.filter(
                product=mirror.id).exists() else "алюминевый профиль"
        },
        'info_for_page': info_for_page,
        "for_header": False
    }

    return render(request, 'products/product_page.html', {'context': context})


def cost(product: Product, size: SizeToProduct = None):
    cost_product = 0
    size = SizeToProduct.objects.filter(product=product.id).filter(initially=True) if size == None else size
    size_length = Size.objects.filter(id=size[0].size.id)[0].lengthMirror / 1000
    size_width = Size.objects.filter(id=size[0].size.id)[0].widthMirror / 1000
    S = size_width * size_length
    P = 0
    if str(product.form) == "Прямоугольник":
        P = (size_width + size_length) * 2
        cost_product += (S * 1600)  # Зеркало
        cost_product += (P * 100)  # ШЛФ
        cost_product += (math.ceil(P / 3) * 900)  # Профиль
    elif str(product.form) == "Круг":
        S = math.pi * (size_length / 2) ** 2
        P = math.pi * 2 * (size_length / 2)
        cost_product += (S * 1600) * (1.2 if size_length > 1200 else 1.5)  # Зеркало
        cost_product += (P * 100) * 1.2  # ШЛФ
    if PlywoodBasisToProduct.objects.filter(product=product.id).exists():
        for i in range(PlywoodBasisToProduct.objects.filter(product=product.id).count()):
            plywood_basis = (
                PlywoodBasis.objects.get(id=PlywoodBasisToProduct.objects.filter(product=product.id)[i].basis.id))
            cost_product += float(max(math.ceil(min((size_length, size_width))
                                                / min((plywood_basis.plywood_length, plywood_basis.plywood_width))),
                                      math.ceil(max((size_length, size_width))
                                                / max((plywood_basis.plywood_length,
                                                       plywood_basis.plywood_width)))) * plywood_basis.price)
            cost_product += float(plywood_basis.cutting) * P  # Резка
            #cost_product += 600  # Расходники
        if not BacklightToProduct.objects.filter(product=product.id).exists():
            cost_product += 4000 if S < 2 else 5000 if S < 3 else 6000
    if BacklightToProduct.objects.filter(product=product.id).exists():
        back_light = \
            TypeBacklight.objects.filter(id=BacklightToProduct.objects.filter(product=product.id)[0].typeBackLight.id)[
                0]
        cost_product += (math.ceil(P / (5 / back_light.quantityBlocks)) * 800) + (
                math.ceil(P / 5) * back_light.cost)  # Световая лента
        cost_product += 1100  # Рассходники
        if PlywoodBasisToProduct.objects.filter(product=product.id).exists():  # Работа
            cost_product += 8250 if S < 1 else 9350 if S < 2 else 10450 if S < 3 else 15000
        else:
            cost_product += 7500 if S < 1 else 8500 if S < 2 else 9500 if S < 3 else 12500

    if FrameMirrorToProduct.objects.filter(product=product.id).exists():
        frame_material = \
            FrameMaterial.objects.filter(id=FrameMirrorToProduct.objects.filter(product=product.id)[0].material.id)[0]
        cost_product += math.ceil(P / frame_material.size_price) * float(frame_material.material_price)  # Материал
        if frame_material.with_dye:
            cost_product += 300 if P < 2 else 600 if P < 3 else 1000
        cost_product += float(frame_material.price_work_less) if S < 1 else float(
            frame_material.price_work_more)  # Работа
        cost_product += float(frame_material.consumables_price)  # Расходники

    if product.pesostruy:
        cost_product += 2700 * S

    cost_product += 500  # Аренда
    cost_product += 1200  # Доставка
    cost_product += 1000  # Транспорт
    cost_product *= 1.18
    cost_product = round(cost_product, -2)
    return f'{cost_product}'
