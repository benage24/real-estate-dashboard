from rest_framework import serializers

from account.models import User
from .models import Manager, Building, Apartment, Tenant, Payment


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #limit the user field to staff
        self.fields['user'].queryset=User.objects.filter(is_admin=True)


class ApartmentSerializer(serializers.ModelSerializer):
    building=BuildingSerializer(read_only=True)

    class Meta:
        model = Apartment
        fields = ['id','apartment_number','rooms','rent_price','status','building']
        # fields = '__all__'
        #
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            request=self.context.get("request")
            user = self.request.user
            if request and user.is_authenticated:
                # available apartment
                self.fields['building'].queryset = Building.objects.filter(user=user)
                print("user",user)



class TenantSerializer(serializers.ModelSerializer):
    apartment = ApartmentSerializer(read_only=True)
    class Meta:
        model = Tenant
        fields = ['id','name','contact','apartment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # available apartment
        self.fields['apartment'].queryset = Apartment.objects.filter(status="available")



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
