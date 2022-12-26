from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..common.models import BaseModel, Currency

__all__ = ["User"]


class User(BaseModel, AbstractUser):
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD)

    def save(self, *args, **kwargs):
        self.username = self.email
        self.set_password(self.password)
        super().save(*args, **kwargs)

    @property
    def budget(self):
        incomes = self.income_set.all().aggregate(Sum("amount"))["amount__sum"]
        expenses = self.expense_set.all().aggregate(Sum("amount"))["amount__sum"]

        return incomes - expenses


@receiver(signal=post_save, sender=User)
def create_default_categories(*args, **kwargs):
    if kwargs.get("created"):
        from ..expenses.management.commands.load_categories import Command

        Command().handle(user_id=kwargs.get("instance").id)
