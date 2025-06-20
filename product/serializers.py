from rest_framework import serializers
from .models import Category, Product

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'price']

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        models = Product
        fields = ['id', 'name', 'slug', 'description', 'image', 'price']




class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image' 'slug']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products']