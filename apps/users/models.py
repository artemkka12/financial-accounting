from django.contrib.auth.models import AbstractUser
from django.db import connection, models
from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from psqlextra.backend.schema import PostgresSchemaEditor

from ..common.models import BaseModel, Currency

__all__ = ["User"]


class User(BaseModel, AbstractUser):
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD)

    @property
    def budget(self):
        incomes = self.income_set.all().aggregate(Sum("amount"))["amount__sum"]
        expenses = self.expense_set.all().aggregate(Sum("amount"))["amount__sum"]

        return incomes - expenses


# noinspection PyUnusedLocal
@receiver(signal=post_save, sender=User)
def user_post_save_handler(instance: User, created: bool, **kwargs):
    if created:
        from ..expenses.management.commands.load_categories import Command
        from ..expenses.models import Expense

        Command().handle(user_id=instance.id)

        schema_editor: PostgresSchemaEditor = connection.schema_editor()
        schema_editor.add_list_partition(model=Expense(), name=instance.username, values=[instance.pk])


# noinspection PyUnusedLocal
@receiver(signal=post_delete, sender=User)
def user_post_delete_handler(instance: User, **kwargs):
    from ..expenses.models import Expense

    schema_editor: PostgresSchemaEditor = connection.schema_editor()
    schema_editor.delete_partition(model=Expense(), name=instance.username)
