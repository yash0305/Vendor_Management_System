from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer

from datetime import datetime, timedelta, date
import random
from faker import Faker 

fake = Faker()


def generate_dummy_vendor_data(num):
    for i in range(num):
        name = fake.company()
        contact_details = fake.phone_number()
        address = fake.address()
        vendor_code = fake.uuid4()  # Generates a random UUID as a vendor code
        on_time_delivery_rate = round(random.uniform(80, 100), 2)  # Random float between 80 and 100
        quality_rating_avg = round(random.uniform(2, 5), 2)  # Random float between 2 and 5 for quality rating
        average_response_time = round(random.uniform(1, 24), 2)  # Random float between 1 and 24 hours
        fulfillment_rate = round(random.uniform(70, 100), 2)  # Random float between 70 and 100

        Vendor.objects.create(
            name= name,
            contact_details= contact_details,
            address= address,
            vendor_code= vendor_code,
            on_time_delivery_rate= on_time_delivery_rate,
            quality_rating_avg= quality_rating_avg,
            average_response_time= average_response_time,
            fulfillment_rate= fulfillment_rate
        )

def generate_dummy_purchase_orders(num_records):
    vendors = Vendor.objects.all()  # Fetching existing vendors or use your logic to retrieve them

    for _ in range(num_records):
        vendor = random.choice(vendors)  # Randomly select a vendor
        po_number = fake.uuid4()  # Generate a random PO number using Faker

        order_date = fake.date_time_this_month(before_now=True, after_now=False)
        delivery_date = order_date + timedelta(days=random.randint(1, 30))

        # Generate dummy items in JSON format
        items = [
            {
                "item_name": fake.word(),
                "price": round(random.uniform(10, 100), 2),
                "quantity": random.randint(1, 20),
            }
            for _ in range(random.randint(1, 5))
        ]

        quantity = sum(item["quantity"] for item in items)

        status_options = ["Pending", "Completed", "Canceled"]
        status = random.choice(status_options)

        issue_date = fake.date_time_this_month(before_now=True, after_now=False)
        acknowledgment_date = delivery_date + timedelta(days=random.randint(-5, 5)) if status == "Completed" else None

        # Creating a PurchaseOrder object with dummy data
        PurchaseOrder.objects.create(
            vendor=vendor,
            po_number=po_number,
            order_date=order_date,
            delivery_date=delivery_date,
            items=items,
            quantity=quantity,
            status=status,
            issue_date=issue_date,
            acknowledgment_date=acknowledgment_date
        )

# Generating 10 dummy purchase orders
# generate_dummy_purchase_orders(4)

def generate_dummy_performance_records(num_records):
    vendors = Vendor.objects.all()  # Fetching existing vendors or use your logic to retrieve them

    for _ in range(num_records):
        vendor = random.choice(vendors)  # Randomly select a vendor
        date = fake.date_time_this_year(before_now=True, after_now=False)  # Generate a random date within the current year

        on_time_delivery_rate = round(random.uniform(80, 100), 2)  # Random on-time delivery rate
        quality_rating_avg = round(random.uniform(3, 5), 2)  # Random quality rating average
        average_response_time = round(random.uniform(1, 10), 2)  # Random average response time
        fulfillment_rate = round(random.uniform(90, 100), 2)  # Random fulfillment rate

        # Creating a PerformanceRecord object with dummy data
        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=date,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )

# Generating 10 dummy performance records
# generate_dummy_performance_records(10)


def index(request):
    # generate_dummy_vendor_data(20)
    # generate_dummy_purchase_orders(20)
    # generate_dummy_performance_records(20)
    
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

class VendorPerformanceAPIView(APIView):
    def get(self, request, uid):
        try:
            vendor = Vendor.objects.get(uid=uid)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

        # Implement logic to calculate performance metrics for the vendor
        # Replace this with your actual calculation logic
        print(vendor.calculate_on_time_delivery_rate())
        print(vendor.calculate_quality_rating_avg())
        print(vendor.calculate_average_response_time())
        print(vendor.calculate_fulfillment_rate())
        
        now = datetime.now()

     


        performance_metrics = {
            'date' : now,
            'vendor' : vendor.uid,
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