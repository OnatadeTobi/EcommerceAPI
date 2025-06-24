import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ecommerceAPI import settings

from .models import Order, OrderItem
from cart.models import Cart


endpoint_secret = settings.WEBHOOK_SECRET


@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if (
    event['type'] == 'checkout.session.completed'
    or event['type'] == 'checkout.session.async_payment_succeeded'
  ):
    session = event['data']['object']
    cart_code = session.get('metadata', {}).get('cart_code')

    fulfill_checkout(session, cart_code)

  return HttpResponse(status=200)


def fulfill_checkout(session, cart_code):
    order = Order.objects.create(stripe_checkout_id=session['id'],
                               amount = session['amount_total'],
                               currency = session['currency'],
                               customer_email = session['customer_email'],
                               status='Paid')
  
    cart = Cart.objects.get(cart_code=cart_code)
    cartitems = cart.cartitems.all()

    for item in cartitems:
        orderitem = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

    cart.delete()