from rest_framework import serializers

from .models import Debt

__all__ = ["DebtSerializer"]


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = "__all__"
