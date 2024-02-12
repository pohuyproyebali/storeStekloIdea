from django.urls import path

from products import views


urlpatterns = [
    path('', views.goods, name='goods'),
    path('<int:sort_pk>/', views.goods, name='goods_sort'),
    path('product/<slug:slug_id>/', views.mirror_page, name='mirror'),
]
