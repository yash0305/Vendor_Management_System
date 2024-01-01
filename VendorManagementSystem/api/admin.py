from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'fulfillment_rate')
    search_fields = ('name', 'vendor_code')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'status', 'delivery_date')
    list_filter = ('vendor', 'status')
    search_fields = ('po_number', 'vendor__name')


@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    list_filter = ('vendor__name', 'date')

    def vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else ''  # Return the vendor's name or empty string if vendor is None

    vendor_name.admin_order_field = 'vendor__name'  # Enable ordering by vendor name