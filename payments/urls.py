from django.urls import path
from .import views

urlpatterns = [
    path('checkout/', views.create_checkout_session, name='checkout'),
]
