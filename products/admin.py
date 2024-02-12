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
        costProduct = 0
        size = SizeToProduct.objects.filter(product=product.id).filter(initially=True)
        sizeLenght = Size.objects.filter(id=size[0].size.id)[0].lengthMirror / 1000
        sizeWidth = Size.objects.filter(id=size[0].size.id)[0].widthMirror / 1000
        S = sizeWidth * sizeLenght
        P = 0
        if str(product.form) == "Прямоугольник":
            P = (sizeWidth + sizeLenght) * 2
            costProduct += (S * 1600)  # Зеркало
            costProduct += (P * 100)  # ШЛФ
            costProduct += (math.ceil(P / 3) * 900)  # Профиль
        elif str(product.form) == "Круг":
            S = math.pi * (sizeLenght / 2) ** 2
            P = math.pi * 2 * (sizeLenght / 2)
            costProduct += (S * 1600) * (1.2 if sizeLenght > 1200 else 1.5)  # Зеркало
            costProduct += (P * 100) * 1.2  # ШЛФ
        if PlywoodBasisToProduct.objects.filter(product=product.id).exists():
            for i in range(PlywoodBasisToProduct.objects.filter(product=product.id).count()):
                plywood_basis = (
                    PlywoodBasis.objects.get(id=PlywoodBasisToProduct.objects.filter(product=product.id)[i].basis.id))
                costProduct += float(max(math.ceil(min((sizeLenght, sizeWidth))
                                                   / min((plywood_basis.plywood_length, plywood_basis.plywood_width))),
                                         math.ceil(max((sizeLenght, sizeWidth))
                                                   / max((plywood_basis.plywood_length,
                                                          plywood_basis.plywood_width)))) * plywood_basis.price)
                costProduct += float(plywood_basis.cutting) * P  # Резка
                #costProduct += 600  # Расходники !!!убрать!!!
                #Кромка
            if not BacklightToProduct.objects.filter(product=product.id).exists():
                costProduct += 4000 if S < 2 else 5000 if S < 3 else 6000
        if BacklightToProduct.objects.filter(product=product.id).exists():
            #Добавить рассеиватель
            backLight = \
                TypeBacklight.objects.filter(
                    id=BacklightToProduct.objects.filter(product=product.id)[0].typeBackLight.id)[
                    0]
            costProduct += (math.ceil(P / (5 / backLight.quantityBlocks)) * 800) + (
                    math.ceil(P / 5) * backLight.cost)  # Световая лента
            costProduct += 1100  # Рассходники
            if PlywoodBasisToProduct.objects.filter(product=product.id).exists():  # Работа
                costProduct += 8250 if S < 1 else 9350 if S < 2 else 10450 if S < 3 else 15000
            else:
                costProduct += 7500 if S < 1 else 8500 if S < 2 else 9500 if S < 3 else 12500

        if FrameMirrorToProduct.objects.filter(product=product.id).exists():
            frame_material = \
                FrameMaterial.objects.filter(id=FrameMirrorToProduct.objects.filter(product=product.id)[0].material.id)[
                    0]
            costProduct += math.ceil(P / frame_material.size_price) * float(frame_material.material_price)  # Материал
            if frame_material.with_dye:
                costProduct += 300 if P < 2 else 600 if P < 3 else 1000  # Краска
            costProduct += float(frame_material.price_work_less) if S < 1 else float(
                frame_material.price_work_more)  # Работа
            costProduct += float(frame_material.consumables_price)  # Расходники

        if product.pesostruy:
            costProduct += 2700 * S

        costProduct += 500  # Аренда
        costProduct += 1200  # Доставка
        costProduct += 1000  # Транспорт
        costProduct *= 1.18
        costProduct = round(costProduct, -2)
        return f'{costProduct}'


admin.site.register(Product, ProductsAdmin)
