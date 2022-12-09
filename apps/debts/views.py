from datetime import date

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Debt
from .serializers import (
    DebtCreateSerializer,
    DebtSerializer,
    MarkAsPaidSerializer,
    PartialPaySerializer,
)


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "second_person"]
    ordering_fields = ["created_at", "amount", "deadline"]
    filterset_fields = {
        "person_id": ["exact"],
        "currency": ["exact"],
        "amount": ["exact", "lte", "gte"],
        "created_at": ["exact", "lte", "gte"],
        "deadline": ["exact", "lte", "gte"],
        "is_paid": ["exact"],
        "type": ["exact"],
    }

    def get_queryset(self):
        return self.queryset.filter(person=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return DebtCreateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(person=self.request.user)

    @action(
        detail=False,
        methods=["GET"],
        url_path="overdue",
        url_name="overdue",
    )
    def overdue(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(deadline__lt=date.today(), is_paid=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["PATCH"],
        url_path="mark-as-paid",
        url_name="mark-as-paid",
        serializer_class=MarkAsPaidSerializer,
    )
    def mark_as_paid(self, request, *args, **kwargs):
        debt = self.get_object()
        debt.is_paid = True
        debt.save(update_fields=["is_paid"])
        serializer = self.get_serializer(debt)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["PATCH"],
        url_path="partial-pay",
        url_name="partial-pay",
        serializer_class=PartialPaySerializer,
    )
    def partial_pay(self, request, *args, **kwargs):
        debt = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        debt.partial_pay(serializer.validated_data.get("amount"))
        serializer = self.get_serializer(debt)
        return Response(serializer.data)
