from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cart, CartItem
from product.models import Product
from .serializers import CartSerializer, CartItemSerializer, CartStatSerializer

# Create your views here.
@api_view(['POST'])
def add_to_cart(request):
    cart_code = request.data.get('cart_code')
    product_id = request.data.get('product_id')

    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)
    cartitem.quantity = 1
    cartitem.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data)



@api_view(['PUT'])
def update_cartitem_quantity(request):
    cartitem_id = request.data.get('item_id')
    quantity = request.data.get('quantity')
    print(request.data)


    quantity = int(quantity)

    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.quantity = quantity
    cartitem.save()
    print(request.data)


    serializer = CartItemSerializer(cartitem)
    print(request.data)

    return Response({'data':serializer.data, 'messaege':'Cart item updated successfully!'})
    



