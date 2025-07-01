from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import CreateAPIView ,ListAPIView
from rest_framework.permissions import IsAuthenticated


from product.pagination import StandardResultPagination
from product.models import Product
from .models import Wishlist
from .serializers import WishlistDisplaySerializer, WishlistSerializer



 
class AddToWishlist(CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        product = get_object_or_404(Product, id=product_id)

        wishlist = Wishlist.objects.filter(user=user, product=product)

        if wishlist.exists():
            wishlist.delete()
            return Response({'detail': 'Wishlist item removed.'}, status=status.HTTP_204_NO_CONTENT)

        new_wishlist = Wishlist.objects.create(user=user, product=product)
        serializer = self.get_serializer(new_wishlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UserWishlistView(ListAPIView):
    serializer_class = WishlistDisplaySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).order_by('created_at')

