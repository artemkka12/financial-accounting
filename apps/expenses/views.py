from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Expense
from .serializers import (
    CategorySerializer,
    CreateCategorySerializer,
    ExpenseSerializer,
    ReportSerializer,
    TotalByCategoriesSerializer,
    TotalSerializer,
)

__all__ = ["ExpenseViewSet", "CategoryViewSet"]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCategorySerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "category__name"]
    ordering_fields = ["created_at", "amount"]
    filterset_fields = {
        "user_id": ["exact"],
        "category": ["exact"],
        "amount": ["exact", "lte", "gte"],
        "created_at": ["exact", "lte", "gte"],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=["GET"],
        url_path="total-spent",
        url_name="total-spent",
        serializer_class=TotalSerializer,
    )
    def total_spent(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.total()
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="total-by-categories",
        url_name="total-by-categories",
        serializer_class=TotalByCategoriesSerializer,
    )
    def total_by_categories(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.total_by_categories()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="report",
        url_name="report",
        serializer_class=ReportSerializer,
    )
    def report(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.report()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)
