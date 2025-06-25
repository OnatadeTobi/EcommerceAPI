from django.urls import path
from .views import AddToWishlist

urlpatterns = [
    path('add-to-wishlist/', AddToWishlist.as_view(), name='add-to-wishlist'),
]
