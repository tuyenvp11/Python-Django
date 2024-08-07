from django.contrib import admin
from .models import *

# Register your models here.

""" admin.site.register(Customer) """
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'sub_category']
    list_filter = ["sub_category"]
admin.site.register(Category, CategoryAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_vendor']
    list_filter = ["name_vendor"]
admin.site.register(Vendor, VendorAdmin)

class ProductAdmin( admin.ModelAdmin):
    list_display = ['id','name', 'name_vendor', 'price']
    list_filter = ["name", "name_vendor", "date_add"]
admin.site.register(Product, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer']
    list_filter = ["customer"]
admin.site.register(Customer, CustomerAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'date_added']
    list_filter = ["order"]
admin.site.register(OrderItem, OrderItemAdmin)

class OrderedAdmin(admin.ModelAdmin):
    list_display = ['id','customer', 'order', 'name', 'address', 'phone', 'date_added']
    list_filter = ["customer"]
admin.site.register(Ordered, OrderedAdmin)


