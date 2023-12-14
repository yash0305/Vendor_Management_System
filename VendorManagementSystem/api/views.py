from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


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
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

        # Implement logic to calculate performance metrics for the vendor
        # Replace this with your actual calculation logic
        performance_metrics = {
            'on_time_delivery_rate': vendor.calculate_on_time_delivery_rate(),
            'quality_rating_avg': vendor.calculate_quality_rating_avg(),
            'average_response_time': vendor.calculate_average_response_time(),
            'fulfillment_rate': vendor.calculate_fulfillment_rate(),
        }

        serializer = HistoricalPerformanceSerializer(data=performance_metrics)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)