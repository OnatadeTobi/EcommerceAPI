from django.db import models
from product.models import Product

# Create your models here.
class Cart(models.Model):
    cart_code = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models .DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_code
    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} X {self.product.name} in cart{self.cart.cart_code}"