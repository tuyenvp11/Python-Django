from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

# view django là các hàm python nhận yêu cầu http và trả về phản hồi http, giống như tài liệu HTML

# Create your views here .
def register(request):
    # Hiển thị giỏ hàng 
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']

    # Hiển thị danh mục
    categories = Category.objects.filter(is_sub=False)

    form = CreateUserForm
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            messages.success(request, ("Bạn đã đăng ký thành công!"))
            form.save()
            return redirect('login')
    context = {
        'form': form,
        'cartItems': cartItems,
        'categories': categories
    }
    return render(request, "app/register.html", context)

def login_user(request):
    # Hiển thị giỏ hàng 
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items':0, 
            'get_cart_total':0
        }
        cartItems = order['get_cart_items']

    # Hiển thị danh mục
    categories = Category.objects.filter(is_sub=False)

    # Xử lý đăng nhập
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Tên đăng nhập hoặc mật khẩu sai!')
   
    context = {
        'cartItems' : cartItems,
        'categories': categories   
    }
    return render(request, "app/login.html", context)

def logout_user(request):
    logout(request)
    return redirect('login')

# Trang chủ
def home(request):
    # hiển thị số mặt hàng trên giỏ hàng 
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        
        cartItems = order.get_cart_items
    else:
        order = {
            'get_cart_items':0, 
            'get_cart_total':0
        }
        cartItems = order['get_cart_items']

    # Hiển thị sản phẩm
    products = Product.objects.all()

    # Hiển thị danh mục
    categories = Category.objects.filter(is_sub=False)

    context = {
        'products' : products, 
        'cartItems': cartItems, 
        'categories': categories
    }
    return render(request, "app/home.html", context)

# Giỏ hàng
def cart(request):
    # hiển thị số mặt hàng trong giỏ hàng
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_items':0, 
            'get_cart_total':0
        }
        cartItems = order['get_cart_items']
    cartItems = order.get_cart_items

    # hiển thị danh mục
    categories = Category.objects.filter(is_sub=False)

    context={
        'items': items, 
        'order' : order, 
        'cartItems': cartItems, 
        'categories': categories
    }
    return render(request, "app/cart.html", context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Customer.objects.get_or_create(customer = customer)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'delete':
        orderItem.quantity = 0
    orderItem.save()
    if orderItem.quantity <= 0 :
        orderItem.delete()

    return JsonResponse('added', safe = False)

# Thanh toán
def checkout(request):
    # hiển thị giỏ hàng
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items':0, 
            'get_cart_total':0
        }
        cartItems = order['get_cart_items']  

    # danh mục
    categories = Category.objects.filter(is_sub=False)

    # xử lý thông tin nhận hàng
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        request.session['name'] = name
        request.session['address'] = address
        request.session['phone'] = phone

        ordered = Ordered.objects.create(
            customer = request.user,
            order = order,
            name = name,
            address = address,
            phone = phone
        )

        del request.session['name'] 
        del request.session['address'] 
        del request.session['phone'] 

        order.orderitem_set.all().delete()    
        order.save()
        return redirect('ordered')

    context={
        'items': items, 
        'order' : order, 
        'cartItems':cartItems, 
        'categories':categories      
    }
    return render(request, "app/checkout.html", context)

# Đơn hàng đã đặt
def ordered(request):
    # hiển thị số mặt hàng trong giỏ hàng
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items':0, 
            'get_cart_total':0
        }
        cartItems = order['get_cart_items']
    
    # danh mục
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    
    #if request.user.is_authenticated:
    ordered = Ordered.objects.all()

    context={
        'items': items, 
        'order': order,
        'ordered': ordered,
        'categories': categories, 
        'active_category':active_category, 
        'cartItems':cartItems
    }

    return render(request, 'app/ordered.html', context)


def search(request):
    # hiển thị số mặt hàng trên giỏ hàng
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items':0, 
            'get_cart_total':0
            }
        cartItems = order['get_cart_items']

    # tìm kiếm
    if request.method == "POST":
        searched = request.POST['searched']
        # truy vấn sản phẩm 
        keys = Product.objects.filter(Q(name__icontains = searched) | Q(detail__icontains = searched))
    
    # hiển thị danh mục
    categories = Category.objects.filter(is_sub=False)

    context = {
        "searched":searched, 
        "keys": keys,
        'cartItems':cartItems, 
        'categories':categories
    }

    return render(request, 'app/search.html', context)

def category(request):
    # hiển thị số mặt hàng trên giỏ hàng
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        cartItems = order.get_cart_items
    else:
        order = {
            'get_cart_items':0, 
            'get_cart_total':0
        }
        cartItems = order['get_cart_items']
    
    # danh mục
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    if active_category:
        product = Product.objects.filter(category__slug = active_category)
    context = {
        'categories': categories, 
        'product' : product, 
        'active_category':active_category, 
        'cartItems':cartItems
    }
    return render(request, 'app/category.html', context)

def detail(request):
    # hiển thị số mặt hàng trên giỏ hàng
    if request.user.is_authenticated:
        customer = request.user
        order, created = Customer.objects.get_or_create(customer = customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    
    # danh mục
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    
    # Chi tiết (detail)
    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)

    context = {
        'products': products,
        'categories': categories, 
        'active_category': active_category, 
        'cartItems': cartItems
    }
    return render(request, 'app/detail.html', context)


