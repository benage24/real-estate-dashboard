from rest_framework.routers import DefaultRouter

from .views import ManagerViewSet, BuildingViewSet, ApartmentViewSet, TenantViewSet, PaymentViewSet

router = DefaultRouter()
# router.register(r'profiles', ProfileViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'buildings', BuildingViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'payments', PaymentViewSet)


urlpatterns = router.urls
