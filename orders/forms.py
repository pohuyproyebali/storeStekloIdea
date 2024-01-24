from django import forms
from .models import Order, ProductToOrders


class OrderForm(forms.ModelForm):
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form__input', 'placeholder': "Почта"
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form__input', 'placeholder': "Имя"}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': "Город"}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': "Номер телефона"})
    )
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form__textarea'}))

    class Meta:
        model = Order
        fields = '__all__'
