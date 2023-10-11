from django.db import models
from account.models import CustomUser as User
from products.models import Product

# Create your models here.

payment_method = (
    ("online", "Online"),
    ("in-shop", "In Shop")
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the cart to a user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    order_id = models.CharField(max_length=20, unique=True)
    method_of_payment = models.CharField(max_length=10, choices=payment_method)


    def __str__(self):
        return f"Order for {self.user.email}"
    
    def total_price(self):
        # Calculate and return the total price of all items in the cart
        total = sum(item.subtotal() for item in self.order_items.all())
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # You need to define your Product model
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order for {self.order.user.email}"
    
    def subtotal(self):
        # Calculate and return the subtotal (price * quantity) for this item
        return self.product.price * self.quantity
