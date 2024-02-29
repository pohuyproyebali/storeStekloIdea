from django.shortcuts import render, redirect


# Create your views here.

def basket_list(request):
    context = {}
    return redirect(request.POST.get('url_form'))


def add_to_basket(request, product_id, size_id=None):
    if request.method == 'POST':
        if not request.session.get('basket'):
            request.session['basket'] = list()
        else:
            request.session['basket'] = list(request.session['basket'])

        basket_ids_list = list()
        for item in request.session['basket']:
            basket_ids_list.append(item['id'])
            basket_ids_list.append(item['size'])
            basket_ids_list.append(item['id_of_many'])

        app_data = {
            'id': product_id,
            'size': size_id,
            'id_of_many': len(request.session['basket']) - [
                (product if product['id'] == product_id else None) for product in request.session['basket']
            ].count(None)
        }

        request.session['basket'].append(app_data)
        request.session.modified = True
        print(request.session['basket'])

    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_basket(request, product_id, id_of_many):

    if request.method == 'POST':

        for item in request.session['basket']:
            if item['id'] == product_id and item['id_of_many'] == id_of_many:
                item.clear()

        while {} in request.session['basket']:
            request.session['basket'].remove({})

        if not request.session['basket']:
            del request.session['basket']

        request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER'))


