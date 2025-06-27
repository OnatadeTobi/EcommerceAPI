from django.urls import path
from .views import AddToWishlist, UserWishlistView

urlpatterns = [
    path('wishlist/', AddToWishlist.as_view(), name='add-to-wishlist'),
    path('my-wishlist/', UserWishlistView.as_view(), name='my-wishlist'),
]
