from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User


class Manager(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="buildings",null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.address})"


class Apartment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
    ]

    building = models.ForeignKey(Building, related_name="apartments", on_delete=models.CASCADE)
    apartment_number = models.CharField(max_length=50)
    rooms = models.IntegerField()
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        unique_together=('building','apartment_number')

    def __str__(self):
        return f"Apt {self.apartment_number} - {self.building.name}"


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    lease_start = models.DateField()
    lease_end = models.DateField()
    apartment = models.OneToOneField(Apartment, related_name="tenant", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('card', 'Card'),
    ]

    tenant = models.ForeignKey(Tenant, related_name="payments", on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, related_name="payments", on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, related_name="payments", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"{self.tenant.name} paid {self.amount} for {self.apartment}"

@receiver(post_save, sender=Tenant)
def update_apartment_status_on_assign(sender, instance, created, **kwargs):

    if created:
        apartment=instance.apartment
        apartment.status="rented"
        apartment.save()

