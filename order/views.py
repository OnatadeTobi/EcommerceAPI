import stripe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from ecommerceAPI import settings
from .models import Order, OrderItem
from cart.models import Cart

endpoint_secret = settings.WEBHOOK_SECRET

CHECKOUT_EVENTS = ['checkout.session.completed', 'checkout.session.async_payment_succeeded']

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    if not sig_header:
        return HttpResponse(status=400)
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)
    
    if event['type'] in CHECKOUT_EVENTS:
        session = event['data']['object']
        cart_code = session.get('metadata', {}).get('cart_code')
        
        if cart_code:
            fulfill_checkout(session, cart_code)
    
    return HttpResponse(status=200)

def fulfill_checkout(session, cart_code):
    # Prevent duplicate orders
    if Order.objects.filter(stripe_checkout_id=session['id']).exists():
        return
    
    cart = get_object_or_404(Cart, cart_code=cart_code)
    cart_items = cart.cartitems.all()
    
    order = Order.objects.create(
        stripe_checkout_id=session['id'],
        amount=session['amount_total'],
        currency=session['currency'],
        customer_email=session['customer_email'],
        status='Paid'
    )
    
    # Create all order items at once 
    order_items = [
        OrderItem(order=order, product=item.product, quantity=item.quantity)
        for item in cart_items
    ]
    OrderItem.objects.bulk_create(order_items)
    
    cart.delete()