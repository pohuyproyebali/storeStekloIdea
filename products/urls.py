from django.urls import path

from products import views


urlpatterns = [
    path('', views.goods, name='goods'),
    path('product/<slug:slug_id>/', views.mirror_page, name='mirror'),
]
