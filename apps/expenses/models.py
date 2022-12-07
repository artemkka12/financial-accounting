from django.db import models
from django.db.models import Sum

from ..attachments.models import Attachment
from ..common.models import BaseModel, Currency
from ..users.models import User


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


class ExpenseQuerySet(models.QuerySet):
    def get_total(self):
        return self.values("currency").annotate(amount=Sum("amount"))

    def get_total_by_category(self):
        categories = Category.objects.filter(id__in=self.values("category"))
        for category in categories:
            category_total = self.filter(category=category).values("currency").annotate(amount=Sum("amount"))
            yield {
                "category": category,
                "total": category_total,
            }


class Expense(BaseModel):
    objects = ExpenseQuerySet.as_manager()

    currency = models.CharField(choices=Currency.choices, default=Currency.USD, max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.amount} {self.currency}"
