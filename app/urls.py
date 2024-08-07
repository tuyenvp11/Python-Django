from django.contrib import admin
from django.urls import path, include
from . import views

# URL này dành riêng cho app 
urlpatterns = [
    path('', views.home, name="home"),
    
    path('register/', views.register, name="register"),

    path('login/', views.login_user, name="login"),

    path('logout/', views.logout_user, name="logout"),

    path('search/', views.search, name="search"),

    path('category/', views.category, name="category"),

    path('detail/', views.detail, name="detail"),

    path('ordered/', views.ordered, name="ordered"),

    path('cart/', views.cart, name="cart"),

    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
]