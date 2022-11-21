from pathlib import Path

from django.db import models

from ..common.models import BaseModel
from ..users.models import User


def upload_to_user_id(instance: "Attachment", filename: str) -> str:
    return Path(f"attachments/{str(instance.user_id)}").joinpath(filename).as_posix()


class Attachment(BaseModel):
    file = models.FileField(upload_to=upload_to_user_id)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)