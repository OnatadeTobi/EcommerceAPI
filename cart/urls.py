from django.urls import path
from .import views

urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('update-cartitem-quantity/', views.update_cartitem_quantity, name='update-cartitem-quantity'),
    path('delete-cartitem/<int:pk>/', views.delete_cartitem, name='delete-cartitem'),
]
