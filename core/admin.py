from django.contrib import admin

from core.models import Manager, Payment, Apartment, Tenant, Building

# Register your models here.
admin.site.register(Manager)
admin.site.register(Payment)
admin.site.register(Apartment)
admin.site.register(Tenant)
admin.site.register(Building)
# admin.site.register(UserProfile)