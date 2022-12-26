from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import CurrentBudgetSerializer, UserRegisterSerializer, UserSerializer

__all__ = ["UserViewSet"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self, *args, **kwargs):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "create":
            return UserRegisterSerializer

        return super().get_serializer_class()

    @action(
        detail=True,
        methods=["GET"],
        url_path="current-budget",
        url_name="current-budget",
        serializer_class=CurrentBudgetSerializer,
    )
    def current_budget(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
