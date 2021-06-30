from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=64, blank=True,null=True)
    productCode= models.CharField(max_length=32,blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    stock = models.IntegerField(default=0, blank=True, null=True)
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created',]

class Cart(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total


class Order(models.Model):
    customername = models.CharField(max_length=200, blank=True, null=True)
    customerphone = models.CharField(max_length=200, blank=True, null=True)
    customeremail = models.EmailField(blank=True, null=True)
    orderitems = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    total_price = models.IntegerField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    class Meta:
        ordering = ['-created',]

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(f'{self.customername}\n{self.customerphone}')
        canvas = Image.new('RGB', (300, 300), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.customername}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total