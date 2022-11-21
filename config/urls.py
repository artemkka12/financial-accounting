from django.contrib import admin
from django.urls import path

from apps.common.helpers import get_swagger_view

schema_view = get_swagger_view()

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
