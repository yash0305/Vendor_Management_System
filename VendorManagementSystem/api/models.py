from django.db import models
import uuid
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db.models import Avg, Count, F, Case, When, Value


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True


class Vendor(BaseModel):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=50)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)



class PurchaseOrder(BaseModel):    
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def calculate_ontime_delivery_rate(self):
        # Calculate on-time delivery rate only if the status is 'completed'
        if self.status == 'Completed':
            # Count the number of completed POs delivered on or before delivery_date
            vendor_instance = Vendor.objects.get(uid=self.vendor.uid)
            delivery_date = timezone.now()
            completed_purchases_before_delivery_date = vendor_instance.purchase_orders.filter(
                status='Completed',
                delivery_date__lte=self.delivery_date
            ).count()
           
            # completed_purchases = PurchaseOrder.objects.filter(
            #     vendor=self.vendor,
            #     status='completed',
            #     delivery_date__lte=self.delivery_date
            # ).count()

            # Count the total number of completed POs for that vendor
            # total_completed_purchases = PurchaseOrder.objects.filter(
            #     vendor=self.vendor,
            #     status='completed'
            # ).count()

            total_completed_purchases = vendor_instance.purchase_orders.filter(status='completed').count()

            # Avoid division by zero
            if total_completed_purchases > 0:
                # Calculate the on-time delivery rate
                on_time_delivery_rate = completed_purchases_before_delivery_date / total_completed_purchases
                
                print(f"on_time_delivery_rate : {on_time_delivery_rate}")
                return on_time_delivery_rate
            else:
                return 0  # Return 0 if there are no completed purchases for the vendor
        else:
            return None  # Return None for other statuses
        

    def update_quality_rating_average(self):
        # Get all completed POs with quality_rating for the vendor

        vendor_instance = Vendor.objects.get(uid=self.vendor.uid)
        # Retrieve completed POs with quality_rating for the vendor
        completed_purchases_with_rating = vendor_instance.purchase_orders.filter(
            status='Completed',
            quality_rating__isnull=False
        )

        # completed_purchases = PurchaseOrder.objects.filter(
        #     vendor=self.vendor,
        #     status='completed',
        #     quality_rating__isnull=False
        # )

        # Calculate the average quality rating for completed POs
        average_quality_rating = completed_purchases_with_rating.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
        
        # Update the vendor's quality_rating_avg
        print(f"average_quality_rating : {average_quality_rating}")

        return average_quality_rating['avg_quality_rating']
        # if average_quality_rating is not None:
        #     self.vendor.quality_rating_avg = average_quality_rating
        #     self.vendor.save()

    def update_average_response_time(self):
        # Get all acknowledged POs for the vendor
        acknowledged_purchases = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            acknowledgment_date__isnull=False
        )

        # Calculate the time difference for each acknowledged PO
        # start_time = datetime(2023, 12, 31, 12, 0, 0)
        # end_time = datetime(2023, 12, 31, 15, 30, 0)
        # duration = end_time - start_time
        # total_seconds = duration.total_seconds()
        response_times = [
            (purchase.acknowledgment_date - purchase.issue_date).total_seconds() / 3600
            for purchase in acknowledged_purchases
        ]

        # Calculate the average response time
        average_response_time = sum(response_times) / len(response_times) if response_times else None

        print(f"average_response_time : {average_response_time}")

        # # Update the vendor's average_response_time
        # if average_response_time is not None:
        #     self.vendor.average_response_time = average_response_time
        #     self.vendor.save()
        return average_response_time

    def update_fulfillment_rate(self):
        vendor_instance = Vendor.objects.get(uid=self.vendor.uid)

        # Count the number of completed POs without issues for the vendor
        # fulfilled_purchases = self.purchase_orders.filter(
        #     status='completed',
        #     issue_date__isnull=False,
        #     acknowledgment_date__isnull=False,
        #     quality_rating__isnull=True  # Assuming 'quality_rating' indicates issues
        # ).count()

        fulfilled_purchases = vendor_instance.purchase_orders.filter(
            status='Completed',
            issue_date__isnull=False,
            acknowledgment_date__isnull=False,
            quality_rating__isnull=True
             ).count()

        # Count the total number of POs issued to the vendor
        total_purchases = vendor_instance.purchase_orders.count()
        # total_purchases = self.purchase_orders.filter(
        #     issue_date__isnull=False
        # ).count()

        # Avoid division by zero
        if total_purchases > 0:
            # Calculate the fulfillment rate

            fulfillment_rate = fulfilled_purchases / total_purchases
            print(f"fulfillment_rate : {fulfillment_rate}")
            return fulfillment_rate
            # self.fulfillment_rate = fulfillment_rate
            # self.save()

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        # Calculate and update the on-time delivery rate each time a PO is saved
        try:
            # getVendorHistoricalPerformance = HistoricalPerformance.objects.get(uid = self.vendor.uid)
            # print(f"getVendorHistoricalPerformance : {getVendorHistoricalPerformance}")

            current_datetime = datetime.now()
            HistoricalPerformance.objects.update_or_create(
                vendor = self.vendor,
                date = current_datetime,
                on_time_delivery_rate = self.calculate_ontime_delivery_rate(),
                quality_rating_avg  = self.update_quality_rating_average() if self.status == 'completed' and self.quality_rating is not None else None,
                average_response_time = self.update_average_response_time() if self.acknowledgment_date is not None else None,
                fulfillment_rate = self.update_fulfillment_rate()
            )
        except ObjectDoesNotExist:
            print("something went wrong")
            
        

        



    
class HistoricalPerformance(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performance')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

   