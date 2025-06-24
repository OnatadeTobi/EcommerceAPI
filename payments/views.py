from rest_framework.decorators import api_view
from rest_framework.response import Response

from cart.models import Cart

import stripe 
from ecommerceAPI import settings

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
def create_checkout_session(request):
    cart_code = request.data.get('cart_code')
    email = request.data.get('email')
    cart = Cart.objects.get(cart_code=cart_code)
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email= email,
            payment_method_types=['card'],


            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': item.product.name},
                        'unit_amount': int(item.product.price * 100),  # Amount in cents
                    },
                    'quantity': item.quantity,
                }
                for item in cart.cartitems.all()
            ] + [
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'VAT Fee'},
                        'unit_amount': 500,  # $5 in cents
                    },
                    'quantity': 1,
                }
            ],


           
            mode='payment',
            #Ensure to configure to your own custom pages
            # success_url="http://localhost:3000/success",
            # cancel_url="http://localhost:3000/cancel",

            success_url="https://next-shop-self.vercel.app/success",
            cancel_url="https://next-shop-self.vercel.app/failed",

            metadata = {"cart_code": cart_code}
        )
        return Response({'data': checkout_session})
    except Exception as e:
        return Response({'error': str(e)}, status=400)