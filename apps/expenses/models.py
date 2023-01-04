from django.db import models
from django.db.models import Sum
from psqlextra.manager import PostgresManager
from psqlextra.models import PostgresPartitionedModel
from psqlextra.query import PostgresQuerySet
from psqlextra.types import PostgresPartitioningMethod

from ..attachments.models import Attachment
from ..common.models import BaseModel
from ..users.models import User

__all__ = [
    "Expense",
    "ExpenseQuerySet",
    "Category",
]


class Category(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(to=Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        unique_together = ("name", "user")


# noinspection PyUnresolvedReferences
class ExpenseQuerySet(PostgresQuerySet):
    def total(self) -> "ExpenseQuerySet":
        return self.aggregate(amount=Sum("amount"))

    def total_by_categories(self) -> "ExpenseQuerySet":
        categories = Category.objects.filter(id__in=self.values("category"))
        for category in categories:
            expenses = self.filter(category=category)
            total = expenses.total()
            yield {
                "category": category,
                "total": total.get("amount"),
            }

    def report(self) -> "ExpenseQuerySet":
        dates = self.dates("created_at", "day")
        for date in dates:
            expenses = self.filter(created_at__date=date)
            total_by_categories = expenses.total_by_categories()
            yield {
                "date": date,
                "total_by_categories": total_by_categories,
            }


class ExpenseManager(PostgresManager.from_queryset(ExpenseQuerySet)):
    ...


class Expense(BaseModel, PostgresPartitionedModel):
    objects = ExpenseManager()

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    partition_key = models.IntegerField(null=True, blank=True)

    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ["partition_key"]

    def __str__(self) -> str:
        return f"{self.category} - {self.amount} {self.user.currency}"

    def save(self, *args, **kwargs):
        self.partition_key = self.user_id
        super().save(*args, **kwargs)
