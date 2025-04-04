from django.contrib import admin
from .models import Product  
from .models import Comment

admin.site.register(Comment)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')  # Отображаем эти поля в списке товаров
    search_fields = ('name',)  # Добавляем поиск по имени товара
    list_filter = ('price',)  # Добавляем фильтрацию по цене

admin.site.register(Product, ProductAdmin)