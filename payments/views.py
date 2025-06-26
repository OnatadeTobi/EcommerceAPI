from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle

from django.shortcuts import get_object_or_404
from decimal import Decimal

import stripe
from ecommerceAPI import settings

from cart.models import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
@throttle_classes([ScopedRateThrottle])
def create_checkout_session(request):
    request.throttle_scope = 'checkout'

    cart_code = request.data.get('cart_code')
    email = request.data.get('email')

    if not cart_code or not email:
        return Response(
            {'detail': 'cart_code and email are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart = get_object_or_404(Cart, cart_code=cart_code)



    try:
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.product.name},
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            }
            for item in cart.cartitems.all()
        ]

        if not line_items:
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_total = sum(item.product.price * item.quantity for item in cart.cartitems.all())
        tax_rate = Decimal(0.025)  # 2.5% tax rate (you can modify it)
        tax_amount = int(cart_total * tax_rate * 100)  # Convert to cents for Stripe

        # Append VAT or any extra fees
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Tax (10%)'},
                'unit_amount': tax_amount,
            },
            'quantity': 1,
        })


        

        session = stripe.checkout.Session.create(
            customer_email=email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            #Add your custom pages
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
            metadata={"cart_code": cart_code}
        )

        return Response({'data': session.url}, status=status.HTTP_200_OK)

    except stripe.error.StripeError as e:
        return Response({'detail': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

    except Exception as e:
        return Response({'detail': 'An unexpected error occurred.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
