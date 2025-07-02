from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle

from .models import Review
from product.models import Product
from .serializers import ReviewSerializer


from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class ReviewListCreateView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review'

    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        email = request.data.get('email')
        rating = request.data.get('rating')
        review_text = request.data.get('review')

        if not email or not product_id or not rating or not review_text:
            return Response({'detail': 'Email, product_id, rating and review_text are required.'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, email=email)

        if Review.objects.filter(product=product, user=user).exists():
            return Response({'detail':'You already reviewed this.'}, status=status.HTTP_400_BAD_REQUEST)
    
        review = Review.objects.create(product=product, user=user, rating=rating, review=review_text)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    
    

class ReviewDetailView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review'

    def get(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def put(self, request, pk):
        review = get_object_or_404(Review, id=pk)

        rating = request.data.get('rating')
        review_text = request.data.get('review')

        if not rating or not review_text:
            return Response({'detail': 'Rating and Review are required.'}, status=status.HTTP_400_BAD_REQUEST)

        review.rating = rating
        review.review = review_text
        review.save()
    
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        review.delete()

        return Response({'detail':'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
