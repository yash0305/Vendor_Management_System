from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor, VendorProfile

@receiver(post_save, sender=Vendor)
def create_vendor_profile(sender, instance, created, **kwargs):
    if created:
        VendorProfile.objects.create(vendor=instance)
