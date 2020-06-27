from django.contrib import admin

# Register your models here. my username: imran and pass: 1122
from .models import Customer,Order,OrderItem,ShippingAddress,Categorey,Product
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','price','is_published','is_mvp','categorey')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    search_fields = ('name','categorey')

class CategoreyAdmin(admin.ModelAdmin):
    list_display = ('id','name','is_published')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    search_fields = ('name',)

admin.site.register(Product,ShopAdmin)
admin.site.register(Categorey,CategoreyAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
