from rest_framework import serializers

from ..attachments.serializers import ShortAttachmentSerializer
from .models import Category, Expense

__all__ = [
    "CategorySerializer",
    "ShortCategorySerializer",
    "CreateCategorySerializer",
    "ExpenseSerializer",
    "TotalSerializer",
    "TotalByCategoriesSerializer",
    "ReportSerializer",
]


class CategorySerializer(serializers.ModelSerializer):
    image = ShortAttachmentSerializer()

    class Meta:
        model = Category
        fields = "__all__"


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "image"]

    def to_representation(self, instance):
        return CategorySerializer(instance).data


class ShortCategorySerializer(serializers.ModelSerializer):
    image = ShortAttachmentSerializer()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "image",
        ]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["amount"]


# noinspection PyAbstractClass
class TotalByCategoriesSerializer(serializers.Serializer):
    category = ShortCategorySerializer()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


# noinspection PyAbstractClass
class ReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_by_categories = TotalByCategoriesSerializer(many=True)
