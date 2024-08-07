from django.contrib import admin
from django.urls import path, include
from . import views

# urls dành riêng cho tasks

urlpatterns = [
    path('', views.admin, name = admin),
]

