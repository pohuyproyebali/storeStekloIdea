from django import forms
from django.shortcuts import redirect

from products.models import Product, SizeToProduct
from .models import Order, ProductToOrders


class OrderForm(forms.ModelForm):
    main_page = False
    class_field = 'form__input' if main_page else 'order-form__input'
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': class_field, 'placeholder': "Почта"
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': class_field, 'placeholder': "Имя"}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': class_field, 'placeholder': "Город"}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': class_field, 'placeholder': "Номер телефона"})
    )
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form__textarea'}))

    def update_style(self, main_page=False):
        class_field = 'form__input' if main_page else 'order-form__input'
        self.fields['phone_number'].widget.attrs.update({'class': class_field})
        self.fields['name'].widget.attrs.update({'class': class_field})
        self.fields['city'].widget.attrs.update({'class': class_field})
        self.fields['user_email'].widget.attrs.update({'class': class_field})
        self.fields['comment'].widget.attrs.update({'class': 'form__textarea' if main_page else 'form__textarea-light'})

    class Meta:
        model = Order
        fields = '__all__'


def order_form_create(request, main_page=False):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        form.update_style(main_page)
        if form.is_valid():
            just_created_order = form.save()
            if request.session.get('basket', None):
                for product in request.session['basket']:
                    ProductToOrders.objects.create(
                        order=just_created_order,
                        product=Product.objects.get(id=product['id']),
                        size=Product.product_manager.all_size(product=product['id'])[
                            product['size'] if product['size'] is not None else 0
                        ]
                    )
                del request.session['basket']
                request.session.modified = True
            return form, redirect(request.path)
    else:
        form = OrderForm()
        form.update_style(main_page)
    return form
