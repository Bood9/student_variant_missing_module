from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('processing', 'Собирается'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
