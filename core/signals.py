# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Tenant

@receiver(post_save, sender=Tenant)
def update_apartment_status_on_assign(sender, instance, created, **kwargs):
    if created:
        apartment=instance.apartment
        apartment.status="rented"
        apartment.save()



@receiver(post_delete, sender=Tenant)
def update_apartment_status_on_remove(sender, instance, **kwargs):
    apartment = instance.apartment
    apartment.status = "available"
    apartment.save()
