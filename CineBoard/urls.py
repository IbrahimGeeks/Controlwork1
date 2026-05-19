from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie/add/', views.MovieCreateView.as_view(), name='movie_create'),
    path('movie/<int:pk>/edit/', views.MovieUpdateView.as_view(), name='movie_update'),
    path('movie/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),
]