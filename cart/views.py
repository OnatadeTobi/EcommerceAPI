from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer

from product.models import Product


class CartView(APIView):
    """
    Handles cart operations:
    - GET: Retrieve user's cart with items
    - POST: Modify cart items (add/subtract/remove)
    Actions:
    - add (default): Increase quantity
    - subtract: Decrease quantity (removes if ≤0)
    - remove: Delete item completely
    """

    permission_classes = [IsAuthenticated]


    def get(self, request):
        """Get full cart with items and totals"""

        cart = get_object_or_404(Cart.objects.prefetch_related("cartitems__product"), user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
  

    def post(self, request):
        """
        Modify cart items.
        Required params:
        - product_id: integer
        Optional params:
        - action: string ('add'|'subtract'|'remove') defaults to 'add'
        """

        product_id = request.data.get("product_id")
        action = request.data.get("action", "add")

        if not product_id:
            return Response({"error": "Product ID required"}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        # Create with quantity=1 or get existing
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0}) 

        # Only modify existing items
        if action == "add":
            cart_item.quantity += 1
        elif action == "subtract":
            cart_item.quantity -= 1
        elif action == "remove":
            cart_item.delete()
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

