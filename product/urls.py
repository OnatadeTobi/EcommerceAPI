from django.urls import path
from .views import HomePageView,  ProductListCreateView, ProductDetailView, CategoryListCreateView, CategoryDetailView, ProductSearch

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),

    path('products/', ProductListCreateView.as_view(), name='product-list'), #Endpoint Example: /api/product-list/?min_price=200&max_price=800&featured=true
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    path('category/', CategoryListCreateView.as_view(), name='category-list'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    path('search/', ProductSearch.as_view(), name='search'), #Endpoint Example: /api/search/?query=iphone
]
