from rest_framework import serializers

from ..attachments.serializers import AttachmentSerializer
from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    image = AttachmentSerializer()

    class Meta:
        model = Category
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["currency", "amount"]


# noinspection PyAbstractClass
class TotalByCategorySerializer(serializers.Serializer):
    category = CategorySerializer()
    total = TotalSerializer(many=True)
