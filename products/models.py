import math

from django.db import models
from django.urls import reverse


# Форма зеркала
class ProductForm(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


# Тип крепления
class FasteningType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


# Manager for Product
class ProductQuerySet(models.QuerySet):
    def all_size(self, product):
        return sorted(
            SizeToProduct.objects.filter(product=product),
            key=lambda item: item.size.widthMirror * item.size.lengthMirror
        )

    def minimal_size(self, product):
        return self.all_size(product)[0]

    def cost(self, product, size=None):
        costProduct = 0
        size = Product.product_manager.minimal_size(product=product) if size is None else size
        size_length = Size.objects.filter(id=size.size.id)[0].lengthMirror / 1000
        size_width = Size.objects.filter(id=size.size.id)[0].widthMirror / 1000
        S = size_width * size_length
        P = 0
        if str(product.form) == "Прямоугольник":
            P = (size_width + size_length) * 2
            costProduct += (S * 1600)  # Зеркало
            costProduct += (P * 100)  # ШЛФ
            costProduct += (math.ceil(P / 3) * 900)  # Профиль
        elif str(product.form) == "Круг":
            S = math.pi * (size_length / 2) ** 2
            P = math.pi * 2 * (size_length / 2)
            costProduct += (S * 1600) * (1.2 if size_length > 1200 else 1.5)  # Зеркало
            costProduct += (P * 100) * 1.2  # ШЛФ
        if PlywoodBasisToProduct.objects.filter(product=product.id).exists():
            for i in range(PlywoodBasisToProduct.objects.filter(product=product.id).count()):
                plywood_basis = (
                    PlywoodBasis.objects.get(id=PlywoodBasisToProduct.objects.filter(product=product.id)[i].basis.id))
                costProduct += float(max(math.ceil(min((size_length, size_width))
                                                   / min((plywood_basis.plywood_length, plywood_basis.plywood_width))),
                                         math.ceil(max((size_length, size_width))
                                                   / max((plywood_basis.plywood_length,
                                                          plywood_basis.plywood_width)))) * plywood_basis.price)
                costProduct += float(plywood_basis.cutting) * P  # Резка
                # costProduct += 600  # Расходники !!!убрать!!!
                # Кромка
            if not BacklightToProduct.objects.filter(product=product.id).exists():
                costProduct += 4000 if S < 2 else 5000 if S < 3 else 6000
        if BacklightToProduct.objects.filter(product=product.id).exists():
            # Добавить рассеиватель
            back_light = \
                TypeBacklight.objects.filter(
                    id=BacklightToProduct.objects.filter(product=product.id)[0].typeBackLight.id)[
                    0]
            costProduct += (math.ceil(P / (5 / back_light.quantityBlocks)) * 800) + (
                    math.ceil(P / 5) * back_light.cost)  # Световая лента
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
        return f'{round(costProduct, -2)}'


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model)

    def all_size(self, product):
        return self.get_queryset().all_size(product=product)

    def minimal_size(self, product):
        return self.get_queryset().minimal_size(product=product)

    def cost(self, product, size=None):
        return self.get_queryset().cost(product=product, size=size)


# Зеркало
class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    form = models.ForeignKey(to=ProductForm, on_delete=models.CASCADE)
    fastening = models.ForeignKey(to=FasteningType, on_delete=models.CASCADE)
    onMainPage = models.BooleanField()
    pesostruy = models.BooleanField()
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    objects = models.Manager()
    product_manager = ProductManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mirror', kwargs={'slug_id': self.slug})


class PlywoodBasis(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.DecimalField(decimal_places=5, max_digits=10)
    plywood_length = models.FloatField()
    plywood_width = models.FloatField()
    cutting = models.DecimalField(decimal_places=5, max_digits=10)

    def __str__(self):
        return f'{self.name} | {self.plywood_width} - {self.plywood_length}'


# База зеркала из Фанеры
class PlywoodBasisToProduct(models.Model):
    basis = models.ForeignKey(to=PlywoodBasis, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.basis} | {self.product}'


# Материал рамы
class FrameMaterial(models.Model):
    name = models.CharField(max_length=128, unique=True)
    consumables_price = models.DecimalField(decimal_places=5, max_digits=10)
    size_price = models.FloatField()
    material_price = models.DecimalField(decimal_places=5, max_digits=10)
    price_work_less = models.DecimalField(decimal_places=5, max_digits=10)
    price_work_more = models.DecimalField(decimal_places=5, max_digits=10)
    with_dye = models.BooleanField()

    def __str__(self):
        return self.name


# Цвет рамы
class FrameColor(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


# Наличие рамы у зеркала
class FrameMirrorToProduct(models.Model):
    material = models.ForeignKey(to=FrameMaterial, on_delete=models.CASCADE)
    color = models.ForeignKey(to=FrameColor, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Материал рамы:{self.material} | Цвет: {self.color} | Название заркала: {self.product}'


# Тип подсветка
class TypeBacklight(models.Model):
    name_for_admin = models.CharField(max_length=128)
    name = models.CharField(max_length=128, unique=True)
    cost = models.IntegerField()
    quantityBlocks = models.IntegerField()

    def __str__(self):
        return f'{self.name_for_admin} | {self.quantityBlocks}'


# Наличие подсветки у зеркала
class BacklightToProduct(models.Model):
    typeBackLight = models.ForeignKey(to=TypeBacklight, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Тип подсветки:{self.typeBackLight} | Название зеркала: {self.product}'


# Размеры зеркала
class Size(models.Model):
    lengthMirror = models.FloatField()
    widthMirror = models.FloatField()

    def __str__(self):
        return f'Длина: {self.lengthMirror} | Ширина: {self.widthMirror}'


# Наличие конкретных размеров у конкретных зеркал
class SizeToProduct(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    size = models.ForeignKey(to=Size, on_delete=models.CASCADE)

    def __str__(self):
        if self == Product.product_manager.minimal_size(product=self.product):
            return f'Размер:{self.size} | Зеркало:{self.product} | Отображение в каталоге: Да'
        else:
            return f'Размер:{self.size} | Зеркало:{self.product} | Отображение в каталоге: Нет'


# Остальные категории
class OtherCategories(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    floorMirror = models.BooleanField()
    dressingRoomMirror = models.BooleanField()
    mosaic = models.BooleanField()

    def __str__(self):
        return f'Напольное: {self.floorMirror} | Гримёрное: {self.dressingRoomMirror} | Мозаичное: {self.mosaic}'


# Фото к зеркалу
class ImageToProduct(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images')
    firstPhoto = models.BooleanField()

    def __str__(self):
        return f'Фото для : {self.product} | Первое: {self.firstPhoto}'
