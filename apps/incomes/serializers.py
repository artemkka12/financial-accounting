from rest_framework import serializers

from .models import Income

__all__ = ["IncomeSerializer"]


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"
