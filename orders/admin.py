from django.contrib import admin
from orders.models import Product, Category, Cart, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','productCode','price','stock']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderId','customername', 'customerphone', 'customeremail','total_price','created']
# Register your models here.
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)