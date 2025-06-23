from django.db import models
from ecommerceAPI import settings
from product.models import Product

# Create your models here.
class Review(models.Model):

    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name}'s review on {self.product.name}"
    
    class Meta:
        #To ensure user can only review a product once and ensure the last updated review is shown
        unique_together = ['user', 'product']
        ordering = ['-created_at']



class ProductRating(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='rating') #OneToOneField to esnure that a product can only have one rating
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.product.name} - {self.average_rating} ({self.total_reviews} reviews)"
