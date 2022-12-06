from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    *router.urls,
    path("users/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
