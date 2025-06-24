from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('userauth.urls')),
    path('api/', include('product.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('review.urls')),
    path('api/', include('wishlist.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('order.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)