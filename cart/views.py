from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Cart, CartItem
from product.models import Product
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.
class CartView(APIView):
    def get(self, request):
        cart_code = request.data.get('cart_code')

        if not cart_code:
            return Response({'detail': 'Cart code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = get_object_or_404(Cart, cart_code=cart_code)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    
  
    
    def post(self, request):
        cart_code = request.data.get('cart_code')
        product_id = request.data.get('product_id')

        if not cart_code or not product_id:
            return Response({'detail': 'Cart Code and Product ID are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = get_object_or_404(Product, id=product_id)

        cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)

        if created:
            cartitem.quantity = 1
        else:
            cartitem.quantity +=1
        cartitem.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



        

    def put(self, request):
        cartitem_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        if not cartitem_id or not quantity:
            return Response({'detail': 'Cart Item ID and Quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({'detail': 'Quantity must be a positive number'}, status=status.HTTP_400_BAD_REQUEST)
            if quantity > 100:  # Set the maximum limit per cart/order
                return Response({'detail': 'Quantity cannot exceed 100'}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({'detail': 'Quantity must be a valid number'}, status=status.HTTP_400_BAD_REQUEST)
        


        cartitem = get_object_or_404(CartItem, id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        
        serializer = CartItemSerializer(cartitem)
        return Response(serializer.data, {'detail':'Cart item updated successfully!'}, status=status.HTTP_200_OK)
    


class CartDelete(APIView):
    def delete(self, request, pk):
        cartitem = get_object_or_404(CartItem, id=pk)
        cartitem.delete()

        return Response({'detail': 'Cart Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)