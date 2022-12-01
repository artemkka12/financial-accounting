from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.common.helpers import get_swagger_view

schema_view = get_swagger_view()

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
                path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
                path("attachments/", include("apps.attachments.urls")),
            ]
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
