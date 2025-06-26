from django.urls import path
from .views import CartView, CartDelete

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart-delete/<int:pk>/', CartDelete.as_view(), name='cart-delete')
]
