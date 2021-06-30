from django import forms
from django.db.models import fields
from orders.models import Product, Order

class StockSearchForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productCode']

class CustomerInformationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customername','customerphone', 'customeremail']