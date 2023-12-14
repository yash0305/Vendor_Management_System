from django.db import models
import uuid
from django.utils import timezone


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

    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        
        on_time_completed_pos = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        
        if total_completed_pos == 0:
            return 0.0
        
        return (on_time_completed_pos / total_completed_pos) * 100

class PurchaseOrder(models.Model):
    po_number = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_order')
    po_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    def calculate_quality_rating_avg(self):
        if self.status == 'completed' and self.quality_rating is not None:
            vendor = self.vendor
            completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
            total_completed_pos = completed_pos.count()
            
            if total_completed_pos > 0:
                quality_rating_avg = completed_pos.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
                vendor.quality_rating_avg = quality_rating_avg
                vendor.save()

    def calculate_average_response_time(self):
        if self.acknowledgment_date is not None:
            vendor = self.vendor
            acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
            total_acknowledged_pos = acknowledged_pos.count()
            
            if total_acknowledged_pos > 0:
                response_times = [(po.acknowledgment_date - po.issue_date).days for po in acknowledged_pos]
                average_response_time = sum(response_times) / total_acknowledged_pos
                vendor.average_response_time = average_response_time
                vendor.save()

    def calculate_fulfillment_rate(self):
        vendor = self.vendor
        all_pos = vendor.purchaseorder_set.all()
        total_pos = all_pos.count()
        fulfilled_pos = all_pos.filter(status='completed', issue_date__isnull=False, delivery_date__isnull=False)
        total_fulfilled_pos = fulfilled_pos.count()
        
        if total_pos > 0:
            fulfillment_rate = (total_fulfilled_pos / total_pos) * 100
            vendor.fulfillment_rate = fulfillment_rate
            vendor.save()


class HistoricalPerformance(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performance')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    # def __str__(self):
    #     return f"{self.vendor.name}"