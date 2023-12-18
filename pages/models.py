from django.db import models


# Тип текста
class TextType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


# Текст страницы
class TextForPage(models.Model):
    name = models.CharField(max_length=128)
    text_type = models.ForeignKey(to=TextType, on_delete=models.CASCADE)
    text = models.TextField(default="")

    def __str__(self):
        return f'Название: {self.name} | Тип: {self.text_type}'


# Тип каринки
class ImageType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


# Картинка для страницы
class ImageForPage(models.Model):
    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to='pages_images')
    image_type = models.ForeignKey(to=ImageType, on_delete=models.CASCADE)

    def __str__(self):
        return f'Название: {self.name} | Тип: {self.image_type}'
