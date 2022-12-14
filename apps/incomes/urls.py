from rest_framework import routers

from .views import IncomeViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"incomes", IncomeViewSet, basename="incomes")

urlpatterns = router.urls
