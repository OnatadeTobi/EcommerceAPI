from rest_framework import serializers
from product.serializers import ProductListSerializer

from .models import Wishlist
from review.serializers import UserSerializer


class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'created_at']


class WishlistDisplaySerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'created_at']