from django.urls import path
from .import views

urlpatterns = [
    path('product-list/', views.product_list, name='product-list'),
    path('product/<slug:slug>/', views.product_detail, name='product-detail'),

    path('category-list/', views.category_list, name='category-list'),
    path('category/<slug:slug>/', views.category_detail, name='category-detail')  
]
