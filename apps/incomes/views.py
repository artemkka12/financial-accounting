from django.contrib.auth import get_user_model
from django.db import models

from apps.common.models import BaseModel, Currency

User = get_user_model()


class Income(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(choices=Currency.choices, default=Currency.USD, max_length=3)
    description = models.TextField()
