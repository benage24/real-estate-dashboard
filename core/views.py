from rest_framework import viewsets,permissions
from rest_framework.permissions import IsAuthenticated

from .models import Manager, Building, Apartment, Tenant, Payment
from .permissions import isSuperadminOrisManager, isSuperadminOrisManagerRO
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
    permission_classes = [isSuperadminOrisManager and permissions.IsAuthenticatedOrReadOnly]
    #
    def get_queryset(self):
        user=self.request.user

        print("user",user)
        if user.manager:
            print("user", Building.objects.filter(user=user))
            return Building.objects.filter(user=user)
        elif user.super_manager:
            return Building.objects.all()
        return Building.objects.none
#
# class ApartmentViewSet(viewsets.ModelViewSet):
#     queryset = Apartment.objects.all()
#     serializer_class = ApartmentSerializer
#     permission_classes = [isSuperadminOrisManager]
#     def get_queryset(self):
#         user=self.request.user
#         building=Building.objects.filter(user=user).first()
#
#         if user.super_manager:
#             return Apartment.objects.all()
#         elif user.manager :
#             queryset=Apartment.objects.filter(building=building)
#             # building_id=queryset.fil
#             print("queryset",queryset)
#             return queryset
#         return Apartment.objects.none


# core/views.py

class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [isSuperadminOrisManager]

    def get_queryset(self):
        user = self.request.user

        # --- 1. Determine the base queryset based on user role ---
        # NOTE: Your original manager logic uses .first(), which only gets one building.
        # This revised logic uses .filter() to handle multiple buildings if the manager
        # is associated with more than one.

        if user.super_manager:
            # Super manager sees all apartments
            queryset = Apartment.objects.all()

        elif user.manager:
            # Manager sees apartments only in the building(s) they manage
            # Find the building(s) managed by the user
            managed_buildings = Building.objects.filter(user=user)

            # Get apartments associated with those managed buildings
            queryset = Apartment.objects.filter(building__in=managed_buildings)

        else:
            # Default to no apartments
            queryset = Apartment.objects.none()

            # --- 2. Apply external filtering by 'building' ID from the URL ---
        # Checks for ?building=<ID> in the URL
        building_id_param = self.request.query_params.get('building')

        if building_id_param:
            # Filter the current queryset by the building ID provided in the URL.
            # 'building_id' is the standard Django lookup for the ForeignKey field 'building'.
            queryset = queryset.filter(building_id=building_id_param)

        return queryset

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [isSuperadminOrisManager]
    def get_queryset(self):
        user = self.request.user
        base_queryset=Tenant.objects.select_related('apartment')
        print(base_queryset)
        if user.super_manager:
            # Super manager sees all tenants
            queryset = Tenant.objects.all()

        elif user.manager:

            managed_buildings = Building.objects.filter(user=user)
            apartment= Apartment.objects.filter(building__in=managed_buildings)
            queryset = Tenant.objects.filter(apartment__in=apartment)

        else:
            # Default to no apartments
            queryset = Tenant.objects.none()
        apartment_id_param = self.request.query_params.get('apartment')

        if apartment_id_param:
            queryset = queryset.filter(apartment__in=apartment_id_param)

        return queryset

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
