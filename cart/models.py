import uuid
from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_code = models.CharField(max_length=11, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models .DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'cart_code')

    def save(self, *args, **kwargs):
        if not self.cart_code:
            #Generate the new cart code
            self.cart_code = uuid.uuid4().hex[:11]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cart_code
    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} X {self.product.name} in cart{self.cart.cart_code}"