from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


def get_swagger_view():
    return get_schema_view(
        openapi.Info(
            title="Finance accounting API",
            default_version="v1",
            description="Finance accounting API",
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
        generator_class=BothHttpAndHttpsSchemaGenerator,
    )
