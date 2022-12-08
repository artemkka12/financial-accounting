from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer

__all__ = ["UserViewSet"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
