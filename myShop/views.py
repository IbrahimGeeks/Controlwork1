from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Category, Product


def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    products = category.products.all()
    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })