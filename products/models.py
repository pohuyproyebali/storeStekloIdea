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
    name_for_admin = models.CharField(max_length=128, unique=True)
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
        return f'Длинна: {self.lengthMirror} | Ширина: {self.widthMirror}'


# Наличие конкретных размеров у конкретных зеркал
class SizeToProduct(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    size = models.ForeignKey(to=Size, on_delete=models.CASCADE)
    initially = models.BooleanField()

    def __str__(self):
        if self.initially:
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
