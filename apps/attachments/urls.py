from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.attachments import views

router = DefaultRouter(trailing_slash=False)
router.register(r"", views.AttachmentViewSet, basename="attachments")

urlpatterns = [
    path("", include(router.urls)),
]
