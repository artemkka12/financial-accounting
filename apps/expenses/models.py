from django.contrib.auth import get_user_model
from django.db import models

from ..common.models import (
    BaseModel,
    Currency,
)

User = get_user_model()


class Category(BaseModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Expense(BaseModel):
    currency = models.CharField(
        choices=Currency.choices,
        default=Currency.USD,
        max_length=3
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} - {self.amount} {self.currency}'
