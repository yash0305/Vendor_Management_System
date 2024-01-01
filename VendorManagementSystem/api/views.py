from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer

from datetime import datetime, timedelta, date

from django.db.models import Sum 
import random
import string



    
def index(request):
    # generate_dummy_vendor_data(10)
    # generate_dummy_purchase_orders(10)
    # generate_dummy_performance_records(10)
    return HttpResponse("Hello, world. You're at the polls index.")


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
