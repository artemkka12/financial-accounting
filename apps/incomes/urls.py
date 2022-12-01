from rest_framework import routers
from views import IncomeViewSet

router = routers.DefaultRouter()

router.register(r"", IncomeViewSet, basename="incomes")

urlpatterns = router.urls
