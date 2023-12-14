from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import index, VendorViewSet, VendorPerformanceAPIView

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', VendorViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("", index, name="index"),
    path('api/vendors/<uuid:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    # Other URL patterns
]

# /api/purchase_orders/:

# /api/vendors/{vendor_id}/performance: