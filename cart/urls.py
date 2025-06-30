from django.urls import path
from .views import CartView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Decorate the viewset at URL config level
cart_view = swagger_auto_schema(
    method='post',
    operation_description="Modify cart items. Actions: add (default), subtract, remove",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'action': openapi.Schema(type=openapi.TYPE_STRING, enum=['add', 'subtract', 'remove'])
        }
    )
)(CartView.as_view())


urlpatterns = [
    path('cart/', CartView.as_view(), name='cart-view'),
]
