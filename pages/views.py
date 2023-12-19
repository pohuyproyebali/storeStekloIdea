from django.shortcuts import render
from pages.models import *
from products.models import Product, SizeToProduct, PlywoodBasisToProduct, TypeBacklight, BacklightToProduct, \
    ImageToProduct

# Create your views here.


info_for_page = {
    'logo': TextForPage.objects.get(text_type=TextType.objects.get(name='Logo')).text,
    'text_for_footer': TextForPage.objects.filter(text_type=TextType.objects.get(name='Titles'))[5].text,
}


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
                    'image': ImageToProduct.objects.get(product=mirror.id, firstPhoto=True).image.url,
                    'mirror_url': mirror.get_absolute_url
                }
                for mirror in mirrors
            }
        ,
        'for_header': True,
        'info_for_page': info_for_page,
        'text_for_page':
            {
                'popular_block': TextForPage.objects.filter(text_type=TextType.objects.get(name='Titles'))[0].text,
                'project_titles_block': TextForPage.objects.filter(text_type=TextType.objects.get(name='Titles'))[1].text,
                'faq_titles_block': TextForPage.objects.filter(text_type=TextType.objects.get(name='Titles'))[2].text,
                'development_process_titles_block': TextForPage.objects.filter(text_type=TextType.objects.get(name='Titles'))[3].text,
                'contact_us_titles_block': TextForPage.objects.filter(text_type=TextType.objects.get(name='Titles'))[4].text,

            }
    }
    return render(request, 'index.html', {'context': context})
