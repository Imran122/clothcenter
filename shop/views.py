from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import datetime
from .models import Customer,Order,OrderItem,ShippingAddress,Categorey,Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from . utils import cookieCart, cartData, guestOrder
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = [ ]
        order = {'get_total_price': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    products = Product.objects.all().filter(is_mvp=True)[:3]
    context = {'products':products, 'cartItems': cartItems}
    return render(request, 'pages/index.html',context)



def shop(request):
    #sob kisu utils a neya gesi aikhane just call kore disi view er jonno shop er
    #niche 2 ta use korsi bcz just view lagbe cart item icon a
    data = cartData(request)
    cartItems = data['cartItems']



    products = Product.objects.all().filter(is_published=True,service_product=False)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {'products':paged_products, 'cartItems': cartItems}
    return render(request, 'pages/shop.html',context)


#service page here........ 


def service(request):
    #sob kisu utils a neya gesi aikhane just call kore disi view er jonno shop er
    #niche 2 ta use korsi bcz just view lagbe cart item icon a
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all().filter(service_product=True)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {'products':paged_products, 'cartItems': cartItems}
    return render(request, 'pages/service.html',context)


#cart page here worked

def cart(request):
    #sob kisu utils a neya gesi aikhane just call kore disi view er jonno cart a
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

            
    context = {'items': items, 'order':order, 'cartItems': cartItems}
    return render(request, 'pages/cart.html',context)

# check out page code is here




def checkout(request):
    #sob kisu utils a neya gesi aikhane just call kore disi view er jonno checkout a
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order':order, 'cartItems': cartItems}
    return render(request, 'pages/checkout.html',context)

# update item cart is here worked
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse("Item is added", safe=False)


#from django.views.decorators.csrf import csrf_exempt

def processOrder(request):
    
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)


    else:
        customer,order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_total_price):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            country = data['shipping']['country'],
            address1 = data['shipping']['address1'],
            address2 = data['shipping']['address2'],
            city = data['shipping']['city'],
            zipcode = data['shipping']['zipcode'],

            )

    return JsonResponse("payment complete", safe=False)
