from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth import get_user_model

from product.models import Product
from .models import Wishlist
from .serializers import WishlistSerializer

User = get_user_model()

# Create your views here.
class AddToWishlist(APIView):
    def post(self, request):
        email = request.data.get('email')
        product_id = request.data.get('product_id')

        if not email or not product_id:
            return Response({'detail': 'Email and product_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        product = get_object_or_404(Product, id=product_id)

        wishlist = Wishlist.objects.filter(user=user, product=product)

        #Handles the deletion of product in the wishlist, it checks if its in the wishlist and if it is, it deletes it
        if wishlist.exists():
            wishlist.delete()
            return Response({'detail':'Wishlist Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
    
        new_wishist = Wishlist.objects.create(user=user, product=product)
        serializer = WishlistSerializer(new_wishist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)