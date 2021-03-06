"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from orders import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path ('purchase/',views.purchase, name='purchase'),
    path('add/<pk>/', views.add_to_cart, name="add"),
    path('cart/',views.cart_view,name="cart"),
    path('remove/<pk>/',views.remove_from_cart,name='remove'),
    path('increase/<pk>/',views.increase_cart, name = 'increase'),
    path('decrease/<pk>/',views.decrease_cart, name = 'decrease'),
    path('checkout/',views.checkout, name = 'checkout'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home')
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
