#ai file ta view.py file er short form,just ai file ta views file a call kore disi
#bar bar ak jinis na likhe ai ak jaiga likhe then seta views er sob jaiga call korsi
import json
from . models import *
import datetime
from .models import Customer,Order,OrderItem,ShippingAddress,Categorey,Product
def cookieCart(request):
    #cookies neya kaj korsi aikhane sob plus minus korar kaj gula kora hoise
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_total_price': 0, 'get_sub_total': 0, 'get_cart_items': 0,'get_discount_price': 0,'get_total_discount_price': 0,'get_discount': 0, 'shipping': False}
    cartItems = order['get_cart_items']
        

        
    for i in cart:
        try:
            #ai khane try use korci jodi ami database thke kono product delete kore di tokon cart a jeno error na ase tai
            cartItems += cart[i]["quantity"]
                
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_sub_total'] += total
            get_sub_total = order['get_sub_total']
            order['get_cart_items'] += cart[i]['quantity']
                

            get_total_discount_price = ((product.price * cart[i]['quantity']) - (product.less_price * cart[i]['quantity']))
                
                
            #find get_total_price is here without discount price 
            order['get_total_price'] += get_total_discount_price
            get_total_price=order['get_total_price']

            #find total discount , sob product er aksathe discount er jogfol ber korsi
                
            order['get_discount'] = get_sub_total - get_total_price
            get_discount = order['get_discount']
                


            item = {
                'product':{
                    'id': product.id,    
                    'name':product.name,
                    'price':product.price,
                    'less_price':product.less_price,
                    'imageURL':product.imageURL,
                     },
                    
                    
                    'quantity':cart[i]['quantity'],
                    'get_sub_total': total,
                    'get_total_discount_price':get_total_discount_price,
                    'get_discount':get_discount,
                    'get_total_price':get_total_price,
                    
                
                    }
            items.append(item)
            if product.service_product == False:
                order['shipping'] = True
        except:
            pass
    return{'cartItems': cartItems, 'order': order, 'items':items}


def cartData(request):
    if request.user.is_authenticated:
        
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items':items}


def guestOrder(request, data):
    
    print('user is not login')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']

    customer,created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            )
    return customer,order
    