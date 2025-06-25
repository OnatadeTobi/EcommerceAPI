from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CategoryListCreateView, CategoryDetailView, ProductSearch

urlpatterns = [
    path('product-list/', ProductListCreateView.as_view(), name='product-list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    path('category-list/', CategoryListCreateView.as_view(), name='category-list'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    path('search/', ProductSearch.as_view(), name='search'), #Endpoint Example: /api/search/?query=iphone
]
