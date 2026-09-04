"""
URL configuration for pharmahub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from products.views import product_list
from products.views import add_to_cart
from django.conf import settings
from django.conf.urls.static import static
from products.views import cart
from products.views import remove_from_cart
from products.views import increase_quantity, decrease_quantity
from products.views import checkout
from django.shortcuts import render
from products.views import orders
from django.contrib.auth import views as auth_views
from products.views import payment
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list),
    path('add-to-cart/<int:product_id>/', add_to_cart),
    path('cart/', cart),
    path('remove-from-cart/<int:product_id>/', remove_from_cart),
    path('increase/<int:product_id>/', increase_quantity),
    path('decrease/<int:product_id>/', decrease_quantity),
    path('checkout/', checkout),
    path('success/', lambda request: render(request, 'success.html')),
    path('orders/', orders),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('payment/', payment),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
