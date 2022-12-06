from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Expense
from .serializers import ExpenseSerializer, TodayExpensesSerializer


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "category__name"]
    ordering_fields = ["created_at", "amount"]
    filterset_fields = {
        "user": ["exact"],
        "currency": ["exact"],
        "category": ["exact"],
        "amount": ["exact", "lte", "gte"],
        "created_at": ["exact", "lte", "gte"],
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(
        detail=False,
        methods=["GET"],
        url_path="today-expenses",
        url_name="today-expenses",
        serializer_class=TodayExpensesSerializer,
    )
    def today_expenses(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        today_expenses = queryset.today_expenses()
        return Response(TodayExpensesSerializer(today_expenses, many=True).data)
