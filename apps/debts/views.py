from models import Debt
from rest_framework import viewsets
from serializers import DebtSerializer


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
