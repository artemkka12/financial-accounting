from rest_framework.routers import DefaultRouter

from .views import DebtViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"debts", DebtViewSet, basename="debts")

urlpatterns = router.urls
