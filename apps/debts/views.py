from rest_framework import viewsets

from .models import Debt
from .serializers import DebtSerializer

__all__ = ["DebtViewSet"]


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
