from django.shortcuts import render
from .models import Order, OrderItem

# Create your views here.

def cart(request):
    template_name = "Aviato/empty-cart.html"
    return render(request, template_name)

def orders(request):

    orders = Order.objects.all()

    context = {
        "orders": orders
    }
    return render(request, "Aviato/order.html", context)

def checkout(request):
    return render(request, "Aviato/checkout.html")

def create_order(request):
    if request.method == "POST":
        pass

    return render(request, "Aviato/create-order.html")