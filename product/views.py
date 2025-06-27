from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, ListAPIView,  RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter

from .models import Product, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, CategoryListSerializer, CategoryDetailSerializer
from .pagination import StandardResultPagination
from .filters import ProductFilter

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class HomePageView(ListAPIView):
    queryset = Product.objects.filter(featured=True).order_by('-created_at')
    pagination_class = StandardResultPagination
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductListSerializer
    pagination_class = StandardResultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductDetailSerializer
        return ProductListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('category', openapi.IN_QUERY, description="Category name", type=openapi.TYPE_STRING),
            openapi.Parameter('featured', openapi.IN_QUERY, description="Filter by featured products", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
        




    
class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategoryListSerializer
    pagination_class = StandardResultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

        
class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug'




class ProductSearch(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description', 'category__name']

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')