from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from product.models import Product
from .models import Wishlist
from .serializers import WishlistSerializer

User = get_user_model()

# Create your views here.
@api_view(['POST'])
def add_to_wishlist(request):
    email = request.data.get('email')
    product_id = request.data.get('product_id')

    user = User.objects.get(email=email)
    product = Product.objects.get(id=product_id)

    wishlist = Wishlist.objects.filter(user=user, product=product)

    #Handles the deletion of product in the wishlist, it checks if its in the wishlist and if it is, it deletes it
    if wishlist:
        wishlist.delete()
        return Response('Wishlist Deleted Successfully', status=204)
    
    new_wishist = Wishlist.objects.create(user=user, product=product)
    serializer = WishlistSerializer(new_wishist)
    return Response(serializer.data)