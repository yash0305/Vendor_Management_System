from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import index, VendorViewSet, PurchaseOrderViewSet, VendorPerformanceAPIView, AcknowledgePurchaseOrderAPIView

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)
# router.register(r'historical_performance', HistoricalPerformanceViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("home", index, name="index"),

    path('vendors/<uuid:uid>', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    path('api/purchase_orders/<int:po_id>', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge-purchase-order'),

  
]

