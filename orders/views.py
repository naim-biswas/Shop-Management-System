from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from .forms import StockSearchForm, CustomerInformationForm
from django.contrib import messages
import random
from orders.models import *
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings




# Create your views here.
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def home (request):
    form = StockSearchForm(request.POST or None)
    product = Product.objects.all()
    context = {
        'form': form,
        'product': product,

    }
    if request.method =='POST':
        product = Product.objects.filter(productCode__iexact = form ['productCode'].value())
        print("product",product)
        context = {
        'form': form,
        'product': product,
        }
    return render(request, 'home.html', context)

def add_to_cart(request,pk):
    item = get_object_or_404(Product, pk=pk)
    stock = item.stock
    print("Stock", stock)
    print("Item")
    print(item)
    order_item = Cart.objects.get_or_create(item=item, purchased=False)
    print("Order Item Object:")
    print(order_item)
    print(order_item[0])
    order_qs = Order.objects.filter( ordered=False)
    print("Order Qs:")
    print(order_qs)
    #print(order_qs[0])
    if order_qs.exists():
        order = order_qs[0]
        print("If Order exist")
        print(order)
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            if order_item[0].quantity < stock:
                order_item[0].save()
                messages.info(request, "This item quantity was updated.")
                return redirect("home")
            else:
                messages.warning(request, 'Stock is not available') 
                return redirect('home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to customer cart.")
            return redirect("home")
    else:
        if order_item[0].quantity < stock:
            order = Order()
            order.save()
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to customer cart.")
            return redirect("home")
        else:
            messages.warning(request, 'Stock is not available')
            return redirect("home")

def cart_view(request):
    carts = Cart.objects.filter(purchased=False)
    orders = Order.objects.filter(ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        print("Total Price = ", order.get_totals)
        return render(request, 'cart.html', context={'carts':carts, 'order':order})
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect("home")

def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter( ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from customer cart")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in customer cart.")
            return redirect("home")
    else:
        messages.info(request, "No active order")
        return redirect("home")

def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    stock = item.stock
    order_qs = Order.objects.filter(ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                if order_item.quantity < stock:
                    order_item.save()
                    messages.info(request, f"{item.name} quantity has been updated")
                    return redirect("cart")
                else:
                    messages.warning(request, f"{item.name}'Stock is not available") 
                    return redirect('cart')
        else:
            messages.info(request, f"{item.name} is not in customer cart")
            return redirect("home")
    else:
        messages.info(request, "No active order")
        return redirect("home")

def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter( ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} item has been removed from customer cart")
                return redirect("cart")
        else:
            messages.info(request, f"{item.name} is not in customer cart")
            return redirect("home")
    else:
        messages.info(request, "No active order")
        return redirect("home")

def checkout(request):
    form = CustomerInformationForm(request.POST or None)
    if request.method =='POST':
        if form.is_valid():
            order_qs = Order.objects.filter(ordered=False)
            order = order_qs[0]
            order.customername = form.cleaned_data['customername']
            order.customerphone = form.cleaned_data['customerphone']
            order.customeremail = form.cleaned_data['customeremail']
            order.save()
            messages.info(request,"Customer Information Added")
            print("Order", order)

    order_qs = Order.objects.filter(ordered=False)
    #print(order_qs)
    order_items = order_qs[0].orderitems.all()
    #print(order_items)
    order_total = order_qs[0].get_totals()
    return render(request, 'checkout.html', context={"form":form, "order_items":order_items, "order_total":order_total})

def purchase(request):
    order_qs = Order.objects.filter(ordered=False)
    order = order_qs[0]
    orderId = random.randint(0,1000)
    order.ordered = True
    order.orderId = orderId
    order.total_price = order.get_totals()
    order.save()
    cart_items = Cart.objects.filter(purchased=False)
    for item in cart_items:
        item.purchased = True
        newstok=item.item.stock-item.quantity
        item.item.stock=newstok
        print( item.item.stock)
        item.item.save()
        item.save()
    print("Qr code ", order.qr_code.url)
    context = {
        'orderId':orderId,
        'cart_items':cart_items,
        'order':order,
        'base_dir': settings.BASE_DIR,
    }
    pdf = render_to_pdf("pdfinvoice.html", context)
    return pdf
    messages.success(request,"Order Successful")
    return render (request,"purchase.html",context) 
