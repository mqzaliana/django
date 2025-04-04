# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from comments import views  # Импортируем представления из приложения comments

urlpatterns = [
    # Путь для админки
    path('admin/', admin.site.urls),

    # Путь для регистрации и входа
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Путь для главной страницы
    path('', views.home, name='home'),

    # Путь для каталога товаров
    path('catalog/', views.catalog, name='catalog'),
    
    # Путь для страницы корзины
    path('product/<int:product_id>/add/', views.add_to_cart, name='add_to_cart'),
    path('korzina/', views.korzina, name='korzina'),

    # Путь для страницы продукта
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Путь для добавления в избранное
    path('product/<int:product_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),

    # Путь для добавления товара в корзину
    path('product/<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),

    # Включение URL-ов приложения comments
    path('comments/', include('comments.urls')),  # Это позволяет использовать URLs из вашего приложения comments

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
