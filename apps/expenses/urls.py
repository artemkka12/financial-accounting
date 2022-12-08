from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ExpenseViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"expenses", ExpenseViewSet, basename="expenses")

urlpatterns = router.urls
