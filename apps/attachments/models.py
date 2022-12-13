import urllib.parse
from pathlib import Path

from django.conf import settings
from django.db import models

from ..common.models import BaseModel
from ..users.models import User

__all__ = ["Attachment"]


def upload_to_user_id(instance: "Attachment", filename: str) -> str:
    return Path(f"user_categories/{str(instance.user_id)}").joinpath(filename).as_posix()


class Attachment(BaseModel):
    file = models.FileField(upload_to=upload_to_user_id, null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.file.name

    @property
    def url(self) -> str:
        if self.file and hasattr(self.file, "url"):
            return urllib.parse.urljoin(settings.SITE_URL, self.file.url)
