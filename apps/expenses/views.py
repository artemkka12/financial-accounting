from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Expense
from .serializers import (
    ExpenseReportSerializer,
    ExpenseSerializer,
    TotalByCategoriesSerializer,
    TotalSerializer,
)


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "category__name"]
    ordering_fields = ["created_at", "amount"]
    filterset_fields = {
        "user_id": ["exact"],
        "currency": ["exact"],
        "category": ["exact"],
        "amount": ["exact", "lte", "gte"],
        "created_at": ["exact", "lte", "gte"],
    }

    @action(
        detail=False,
        methods=["GET"],
        url_path="total-spent",
        url_name="total-spent",
    )
    def total_spent(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.get_total()
        serializer = TotalSerializer(data, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="total-by-categories",
        url_name="total-by-categories",
    )
    def total_by_categories(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.get_total_by_category()
        serializer = TotalByCategoriesSerializer(data, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="report",
        url_name="report",
    )
    def report(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.get_report()
        serializer = ExpenseReportSerializer(data, many=True)
        return Response(serializer.data)
