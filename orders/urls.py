from . import views
from django.urls import path

app_name = "orders"


urlpatterns = [
    path("", views.orders, name="orders"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("create-order",views.create_order, name="create-order"),
]
