from rest_framework.routers import DefaultRouter

from .views import AttachmentViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"attachments", AttachmentViewSet, basename="attachments")

urlpatterns = router.urls
