from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from .models import PurchaseOrder
from datetime import datetime


# # Calculate On-Time Delivery Rate
# def calculate_on_time_delivery_rate(vendor):
#     print(f"v = {vendor} ")
#     # print(f"status = {status} ")

#     completed_on_time = PurchaseOrder.objects.filter(
#         vendor=vendor,
#         status='completed',
#         delivery_date__lte=F('completion_date')
#     ).count()
#     total_completed = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
#     return (completed_on_time / total_completed) if total_completed > 0 else 0.0

# # Calculate Quality Rating Average
# def calculate_quality_rating_average(vendor):
#     return PurchaseOrder.objects.filter(vendor=vendor, status='completed').aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0.0

# # Calculate Average Response Time
# def calculate_average_response_time(vendor):
#     avg_response_time = PurchaseOrder.objects.filter(
#         vendor=vendor,
#         acknowledgment_date__isnull=False,
#         issue_date__isnull=False
#     ).annotate(
#         response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
#     ).aggregate(avg_time=Avg('response_time'))['avg_time']
#     return avg_response_time.total_seconds() if avg_response_time else 0.0

# # Calculate Fulfilment Rate
# def calculate_fulfilment_rate(vendor):
#     successfully_fulfilled = PurchaseOrder.objects.filter(vendor=vendor, status='completed', has_issues=False).count()
#     total_issued = PurchaseOrder.objects.filter(vendor=vendor).count()
#     return (successfully_fulfilled / total_issued) if total_issued > 0 else 0.0


def calculate_on_time_delivery_rate(completed_pos, total_pos):
    on_time_deliveries = 0
    for po in completed_pos:
        if po.delivery_date <= po.completion_date:
            on_time_deliveries += 1
    return (on_time_deliveries / total_pos) * 100 if total_pos > 0 else 0

def calculate_quality_rating_average(completed_pos):
    total_rating = 0
    for po in completed_pos:
        total_rating += po.quality_rating
    return (total_rating / len(completed_pos)) if completed_pos else 0

def calculate_average_response_time(issued_pos):
    total_response_time = 0
    for po in issued_pos:
        total_response_time += (po.acknowledgment_date - po.issue_date).days
    return (total_response_time / len(issued_pos)) if issued_pos else 0

def calculate_fulfillment_rate(issued_pos, completed_pos):
    return (len(completed_pos) / len(issued_pos)) * 100 if issued_pos else 0
