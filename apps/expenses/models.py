from django.db import models
from django.db.models import Sum

from ..attachments.models import Attachment
from ..common.models import BaseModel, Currency
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
class ExpenseQuerySet(models.QuerySet):
    def total(self) -> "ExpenseQuerySet":
        return self.values("currency").annotate(amount=Sum("amount"))

    def total_by_categories(self) -> "ExpenseQuerySet":
        categories = Category.objects.filter(id__in=self.values("category"))
        for category in categories:
            expenses = self.filter(category=category)
            total = expenses.total()
            yield {
                "category": category,
                "total": total,
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


class Expense(BaseModel):
    objects = ExpenseQuerySet.as_manager()

    currency = models.CharField(choices=Currency.choices, default=Currency.USD, max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.category} - {self.amount} {self.currency}"
