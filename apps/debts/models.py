from django.db import models

from ..common.models import BaseModel
from ..users.models import User

__all__ = ["Debt", "DebtType"]


class DebtType(models.TextChoices):
    BORROW = "BORROW", "BORROW"
    LEND = "LEND", "LEND"


class Debt(BaseModel):
    type = models.CharField(choices=DebtType.choices, max_length=32, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    partial_paid = models.BooleanField(default=False)
    partial_paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    second_person = models.CharField(max_length=254, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.amount}"

    @property
    def partial_paid_amount_percent(self):
        return self.partial_paid_amount / self.amount * 100

    def partial_pay(self, amount):
        self.partial_paid = True
        self.partial_paid_amount += amount

        if self.partial_paid_amount >= self.amount:
            self.is_paid = True
            self.partial_paid_amount = self.amount

        self.save(update_fields=["partial_paid", "partial_paid_amount", "is_paid"])

    def mark_as_paid(self):
        self.is_paid = True
        self.partial_paid = True
        self.partial_paid_amount = self.amount
        self.save(update_fields=["is_paid", "partial_paid", "partial_paid_amount"])
