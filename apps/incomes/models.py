from django.db import models

from ..common.models import BaseModel, Currency
from ..users.models import User

__all__ = ["Income"]


class Income(BaseModel):
    currency = models.CharField(choices=Currency.choices, default=Currency.USD, max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} {self.currency}"
