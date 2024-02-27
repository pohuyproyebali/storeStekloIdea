from django.urls import path, include

from products import views


urlpatterns = [
    path('', views.goods, name='goods'),
    path('<int:sort_pk>/', views.goods, name='goods_sort'),
    path('product/', include([
        path('<slug:slug_id>/', views.mirror_page, name='mirror'),
        path('<slug:slug_id>/<int:size_id>', views.mirror_page, name='mirror_size'),]))
]
