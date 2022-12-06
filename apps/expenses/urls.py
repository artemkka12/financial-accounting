from rest_framework.routers import DefaultRouter

from .views import ExpenseViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"expenses", ExpenseViewSet, basename="expenses")

urlpatterns = router.urls
