from rest_framework import serializers

from .models import User

__all__ = ["UserSerializer", "CurrentBudgetSerializer"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# noinspection PyAbstractClass
class CurrentBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["budget"]
