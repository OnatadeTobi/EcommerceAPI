from django.urls import path
from .import views

urlpatterns = [
    path('add-review/', views.add_review, name='add-review'),
    path('update-review/<int:pk>', views.update_review, name='update-review'),
]
