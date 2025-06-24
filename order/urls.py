from django.urls import path
from .import views

urlpatterns = [
    path('webhook/', views.my_webhook_view, name='webhooks'),
]
