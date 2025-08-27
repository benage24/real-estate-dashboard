from rest_framework import viewsets
from .models import Manager, Building, Apartment, Tenant, Payment
from .serializers import ManagerSerializer, BuildingSerializer, ApartmentSerializer, TenantSerializer, \
    PaymentSerializer


# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = ProfileSerializer

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    #
    # def get_queryset(self):
    #     user=self.queryset.user
    #     print("user",user)
    #     if user.is_staff():
    #         print("manager")
    #         return Building.objects.filter(is_staff=True)
    #     elif user.has_perms():
    #         return self.queryset

class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
