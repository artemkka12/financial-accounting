from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..common.models import BaseModel

__all__ = ["User"]


class User(BaseModel, AbstractUser):
    pass


@receiver(signal=post_save, sender=User)
def create_default_categories(*args, **kwargs):
    if kwargs.get("created"):
        from ..expenses.management.commands.load_categories import Command

        Command().handle(user_id=kwargs.get("instance").id)
