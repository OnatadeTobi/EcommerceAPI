from django.urls import path
from .views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('review/', ReviewListCreateView.as_view(), name='add-review'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
