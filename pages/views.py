from django.shortcuts import render
from pages.models import *
from products.models import Product, SizeToProduct, PlywoodBasisToProduct, TypeBacklight, BacklightToProduct, \
    ImageToProduct


# Create your views here.


def main_page(request):
    mirrors = Product.objects.filter(onMainPage=True)
    context = {
        'image_next_to_the_slogan': ImageForPage.objects.get(
            image_type=ImageType.objects.get(name="Image next to the slogan on main page").id
        ).image.url,
        'mirrors':
            {
                mirror.name: {
                    'name': mirror.name,
                    'size': SizeToProduct.objects.get(product=mirror.id, initially=True).size,
                    'basis': "фанера" if PlywoodBasisToProduct.objects.filter(product=mirror.id).exists()
                    else "алюминевый профиль",
                    "back_light": (
                        TypeBacklight.objects.get(
                            id=BacklightToProduct.objects.get(product=mirror.id).typeBackLight.id).name if
                        BacklightToProduct.objects.filter(product=mirror.id).exists() else "нет"
                    ).lower(),
                    'image': ImageToProduct.objects.get(product=mirror.id, firstPhoto=True).image.url
                }
                for mirror in mirrors
            }
        ,
        'for_header': True
    }
    return render(request, 'index.html', {'context': context})
