from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Categorey(models.Model):
    name = models.CharField(max_length=200)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
# Create your models here.
class Product(models.Model):
    categorey = models.ForeignKey(Categorey,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    less_price = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    is_mvp = models.BooleanField(default=False)
    service_product = models.BooleanField(default=False, null=True, blank=False)
    is_published = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')

    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ' '
        return url

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200, null=True)



    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.service_product == False:
                shipping = True
        return shipping

        #discount price total ta neya kaj korsi view te show korar jonno
    @property
    def get_discount(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_discount_price for item in orderitems ])
        return total

        #finding total price where minus kora hoise discount then total price and seta view te show ar jonno
    @property
    def get_total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total_discount_price for item in orderitems ])
        return total

    #finding sub total price , without discount price and seta view te show ar jonno
    @property
    def get_sub_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems ])
        return total

# total koita item ase cart a seta view the show ar jonno
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems ])
        return total 


    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.product.name

        #discount price ber korci total ta
    @property
    def get_discount_price(self):
        total= self.product.less_price * self.quantity
        return total


        #aikhane sub total price ber korsi discount sara 
    @property
    def get_total(self):
        total= self.product.price * self.quantity
        return total
    #discount bat dia item gular specific price ber kora hoise
    @property
    def get_total_discount_price(self):
        total= ((self.product.price * self.quantity) - (self.product.less_price * self.quantity))
        return total

    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.CharField(max_length=200,null=True)
    address1 = models.CharField(max_length=200,null=True)
    address2 = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    
    
    def __str__(self):
        return self.address1

