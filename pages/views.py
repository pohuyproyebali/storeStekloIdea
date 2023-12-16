from django.shortcuts import render


# Create your views here.
def main_page(request):
    context = {
        'for_header': True
    }
    return render(request, 'index.html', {'context': context})
