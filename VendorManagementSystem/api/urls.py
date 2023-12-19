from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import index, VendorViewSet, VendorPerformanceAPIView, PurchaseOrderViewSet, HistoricalPerformanceViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)
router.register(r'historical_performance', HistoricalPerformanceViewSet)



urlpatterns = [
    path("", include(router.urls)),
    path("home", index, name="index"),
    # path('vendors/<uuid:uid>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    path('vendors/<uuid:uid>/performance/', VendorPerformanceAPIView, name='vendor-performance'),
    # Other URL patterns
]

# /api/purchase_orders/:

# /api/vendors/{vendor_id}/performance: