from rest_framework import serializers

from ..attachments.serializers import ShortAttachmentSerializer
from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    image = ShortAttachmentSerializer()

    class Meta:
        model = Category
        fields = "__all__"


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
        fields = ["currency", "amount"]


# noinspection PyAbstractClass
class TotalByCategoriesSerializer(serializers.Serializer):
    category = ShortCategorySerializer()
    total = TotalSerializer(many=True)


# noinspection PyAbstractClass
class ExpenseReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_by_categories = TotalByCategoriesSerializer(many=True)
