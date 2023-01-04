from rest_framework import serializers

from .models import User

__all__ = [
    "UserSerializer",
    "CurrentBudgetSerializer",
    "UserRegisterSerializer",
]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# noinspection PyAbstractClass
class CurrentBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["budget"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password", "currency"]
