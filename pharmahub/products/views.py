from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

from .models import Cart, Product
from django.shortcuts import redirect

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    Cart.objects.create(product=product)
    return redirect('/')
from django.shortcuts import redirect
from .models import Product

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('/')


from django.shortcuts import render
from .models import Product

def cart(request):
    cart = request.session.get('cart', [])
    
    products = Product.objects.filter(id__in=cart)
    
    total = 0
    for product in products:
        total += product.price

    return render(request, "cart.html", {
        "products": products,
        "total": total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id in cart:
        cart.remove(product_id)

    request.session['cart'] = cart

    return redirect('/cart/')

from django.shortcuts import redirect

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1

    request.session['cart'] = cart

    return redirect('/cart/')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] -= 1

        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]

    request.session['cart'] = cart

    return redirect('/cart/')

from .models import Product, Order
from django.shortcuts import render, redirect

def checkout(request):

    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        for product in products:
            quantity = cart[str(product.id)]

            Order.objects.create(
                name=name,
                address=address,
                phone=phone,
                product=product,
                quantity=quantity,
                price=product.price
            )

        request.session['cart'] = {}

        return redirect('/success/')

    return render(request, "checkout.html", {"products": products})

def orders(request):
    orders = Order.objects.all()
    return render(request, "orders.html", {"orders": orders})

def product_list(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'products.html', {'products': products})

import razorpay
from django.conf import settings
from django.shortcuts import render

def payment(request):

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    data = {
        "amount": 50000,
        "currency": "INR",
        "payment_capture": "1"
    }

    order = client.order.create(data=data)

    context = {
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": data["amount"]
    }

    return render(request, "payment.html", context)

def checkout(request):

    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        total += product.price * quantity

    return render(request, "checkout.html", {
        "products": products,
        "total": total
    })