from rest_framework.routers import DefaultRouter

from .views import DebtViewSet

router = DefaultRouter()

router.register(r"", DebtViewSet, basename="debts")

urlpatterns = router.urls
