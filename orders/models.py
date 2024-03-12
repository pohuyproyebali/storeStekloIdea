from django.db import models

from products.models import Product, SizeToProduct


class Order(models.Model):
    name = models.CharField(max_length=128)
    done = models.BooleanField()
    user_email = models.EmailField(max_length=254)
    city = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    comment = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} из города {self.city} | Выполнен: {self.done}'


class ProductToOrders(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    size = models.ForeignKey(to=SizeToProduct, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f'Зеркало: {self.product} | Заказ: {self.order} | Выполнен: {self.done} | Размер: {self.size.size}'
