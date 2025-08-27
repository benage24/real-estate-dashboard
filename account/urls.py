from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import CustomTokenObtainPairView, UserViewSet, UserCreateView

router = DefaultRouter()
router.register('user', UserViewSet)
# router.register('permission', CustomPermissionViewSet)
urlpatterns = [
                  path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('create/', UserCreateView.as_view(), name='create-user'),

              ] + router.urls