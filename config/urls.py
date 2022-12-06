from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.common.helpers import get_swagger_view

schema_view = get_swagger_view()

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
                path("", include("apps.attachments.urls")),
                path("", include("apps.debts.urls")),
                path("", include("apps.expenses.urls")),
                path("", include("apps.incomes.urls")),
                path("", include("apps.users.urls")),
            ]
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
