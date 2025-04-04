from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Модель комментариев
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created_at}'

# Модель продукта
class Product(models.Model):
    name = models.CharField(max_length=100)  # Название товара
    description = models.TextField()  # Описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара
    image = models.ImageField(upload_to='products/')  # Изображение товара
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания товара

    def __str__(self):
        return self.name

# Модель карточки
class Card(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Модель избранного
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Уникальное ограничение на сочетание user и product

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

# Модель корзины
class Korzina(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='korzina')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Пользователь может добавить продукт в корзину только один раз

    def __str__(self):
        return f"Корзина пользователя {self.user.username}: {self.product.name} x {self.quantity}"

    def get_total_price(self):
        """Метод для получения стоимости товара с учетом количества"""
        return self.product.price * self.quantity

    @staticmethod
    def get_cart_total(user):
        """Метод для получения общей стоимости всех товаров в корзине пользователя"""
        cart_items = Korzina.objects.filter(user=user)
        return sum(item.get_total_price() for item in cart_items)
