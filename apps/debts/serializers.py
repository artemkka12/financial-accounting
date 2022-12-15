from rest_framework import serializers

from .models import Debt

__all__ = [
    "DebtSerializer",
    "PartialPaySerializer",
    "DebtCreateSerializer",
]


# noinspection PyMethodMayBeStatic
class DebtSerializer(serializers.ModelSerializer):
    paid_percent = serializers.SerializerMethodField()

    class Meta:
        model = Debt
        fields = "__all__"

    def get_paid_percent(self, obj):
        return obj.partial_paid_amount / obj.amount * 100


class DebtCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = ["amount", "description", "type", "second_person", "deadline"]


# noinspection PyAbstractClass
class PartialPaySerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
