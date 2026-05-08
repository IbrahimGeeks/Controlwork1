from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list_view, name='categories'),
    path('products/', views.product_list_view, name='products'),
    path('category/<int:category_id>/', views.category_products_view, name='category_products'),
]