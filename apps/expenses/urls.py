from rest_framework.routers import DefaultRouter

from .views import ExpenseViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"", ExpenseViewSet, basename="expenses")

urlpatterns = router.urls
