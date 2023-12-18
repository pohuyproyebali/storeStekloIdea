from django.shortcuts import render
from pages.models import *


# Create your views here.

def main_page(request):
    context = {
        'image_next_to_the_slogan': ImageForPage.objects.get(
            image_type=ImageType.objects.get(name="Image next to the slogan on main page").id
        ).image.url,
        'for_header': True
    }
    return render(request, 'index.html', {'context': context})
