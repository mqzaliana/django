from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Card, Comment, Product, Favorite, Korzina
from .forms import CommentForm


# Главная страница
def home(request):
    is_admin = request.user.is_authenticated and request.user.groups.filter(name='администраторы').exists()
    comments = Comment.objects.all().order_by('-created_at') if request.user.is_authenticated else []
    form = CommentForm() if request.user.is_authenticated else None
    extra_content = "Административный контент" if is_admin else ""
    products = Product.objects.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('home')
    
    return render(request, 'comments/home.html', {
        'form': form,
        'comments': comments,
        'extra_content': extra_content,
        'products': products
    })

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Авторизация пользователя
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Выход из системы
def logout_view(request):
    logout(request)
    return redirect('home')

# Каталог товаров
def catalog(request):
    products = Product.objects.all() 
    return render(request, 'comments/catalog.html', {'products': products})

# Детали карточки
def card_detail(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    comments = card.comments.all()
    form = CommentForm(request.POST or None)
    
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.card = card
        new_comment.user = request.user
        new_comment.save()
        return redirect('card_detail', card_id=card.id)
    
    return render(request, 'comments/card_detail.html', {
        'card': card,
        'comments': comments,
        'form': form,
    })

# Добавить в избранное
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        if not Favorite.objects.filter(user=request.user, product=product).exists():
            Favorite.objects.create(user=request.user, product=product)
    return redirect('catalog')

# Детали продукта
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'comments/product_detail.html', {'product': product})

# Добавление комментария
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_page')
    else:
        form = CommentForm()
    return render(request, 'comments/add_comment.html', {'form': form})


def korzina(request):
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        products_in_cart = Korzina.objects.filter(user=request.user)
    else:
        products_in_cart = []  # Если пользователь не авторизован, корзина пуста

    return render(request, 'comments/korzina.html', {'products_in_cart': products_in_cart})

# Добавление товара в корзину
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        # Если товара еще нет в корзине, добавляем его
        if not Korzina.objects.filter(user=request.user, product=product).exists():
            Korzina.objects.create(user=request.user, product=product, quantity=1)
    return redirect('korzina')

