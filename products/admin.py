from django.contrib import admin
import math

from products.models import *

admin.site.register(ProductForm)
admin.site.register(FasteningType)
admin.site.register(PlywoodBasis)
admin.site.register(PlywoodBasisToProduct)
admin.site.register(FrameMaterial)
admin.site.register(FrameColor)
admin.site.register(FrameMirrorToProduct)
admin.site.register(TypeBacklight)
admin.site.register(BacklightToProduct)
admin.site.register(Size)
admin.site.register(SizeToProduct)
admin.site.register(OtherCategories)
admin.site.register(ImageToProduct)


def my_id(product: Product):
    id_for_admin = product.id
    return f'{id_for_admin}'


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'form', 'onMainPage', 'cost')
    prepopulated_fields = {'slug': ('name',)}

    def my_id(self, product: Product):
        id_for_admin = product.id
        return f'{id_for_admin}'

    def cost(self, product: Product):
        return f'{Product.product_manager.cost(product=product)}'


admin.site.register(Product, ProductsAdmin)
