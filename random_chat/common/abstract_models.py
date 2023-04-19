import uuid
from uuid import UUID
from typing import Union

from django.db import models


class AbstractExternalID(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True

    def get_external_id(self, hex=False) -> Union[UUID, str]:
        return self.external_id.hex if hex else self.external_id


class AbstractDateTimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class AbstractDelete(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
