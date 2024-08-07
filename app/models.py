from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# model django là một bảng trong cơ sở dữ liệu
# Create your models here.

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

""" class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name """


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
class Vendor(models.Model):
    name_vendor = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name_vendor

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    #price_purchase = models.FloatField()
    #price_sell = models.FloatField()
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    name_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=False) 
    detail = models.TextField(null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    # hàm truyền đường dẫn image url
    @property
    def ImageURL(self):
        try:
            url= self.image.url
        except:
            url = ''
        return url
    
class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False) 
    date_order = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    # Tao ham dem so luong hang hoa
    @property
    def get_cart_items(self):
        # lay tat ca cua order item su dung phuong thuc set_all()
        orderitems = self.orderitem_set.all()
        # su dung ham sum tinh tong so luong don hang
        total = sum([item.quantity for item in orderitems])
        return total
    
    # Tao ham tinh tong tien 
    @property
    def get_cart_total(self):
        # lay tat ca cua order item su dung phuong thuc set_all()
        orderitems = self.orderitem_set.all()
        # su dung ham sum tinh tong tien va lay phuong thuc get total cua ham get_total trong class orderitem
        # Moi lan dat hang thi so tien se duoc nhan len theo so luong
        total = sum([item.get_total for item in orderitems])
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    order = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order) 

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Ordered(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False) 
    order = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    #status = models.CharField(default=False, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address





