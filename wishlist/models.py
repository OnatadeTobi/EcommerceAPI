from django.db import models
from ecommerceAPI import settings
from product.models import Product


# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #To ensure the product in wishlist can only be added once
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.first_name} - {self.product.name}"