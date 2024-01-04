from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from datetime import datetime

    
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            # Assuming vendor_id is the primary key of the Vendor model
            vendor = Vendor.objects.get(id=vendor_id)
            performance_metrics = HistoricalPerformance.objects.filter(vendor=vendor)
            serializer = HistoricalPerformanceSerializer(performance_metrics, many=True)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        

class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)

            # Check if the purchase order is already acknowledged
            if purchase_order.acknowledgment_date:
                return Response({"error": "Purchase order already acknowledged"}, status=status.HTTP_400_BAD_REQUEST)

            # Update acknowledgment_date to the current datetime
            purchase_order.acknowledgment_date = datetime.now()
            purchase_order.save()

           
            return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)