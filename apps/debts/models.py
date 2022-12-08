from django.db import models

from ..common.models import BaseModel, Currency
from ..users.models import User

__all__ = ["Debt"]


class Debt(BaseModel):
    class DebtType(models.TextChoices):
        BORROW = "Borrow", "Borrow"
        LEND = "Lend", "Lend"

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(choices=Currency.choices, max_length=3, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    type = models.CharField(choices=DebtType.choices, max_length=32, null=True, blank=True)
    person = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    second_person = models.CharField(max_length=254, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.person} - {self.amount}"
