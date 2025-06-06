import logging
import uuid

from django.core.exceptions import FieldError
from django.db import models


class GenericBaseModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, null=False, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def model_to_dict(self) -> dict:
        try:
            # Handle regular fields
            data = {
                field.name: getattr(self, field.name) for field in self._meta.fields
            }
            # Handle many-to-many fields
            for field in self._meta.many_to_many:
                data[field.name] = getattr(self, field.name)
            return data
        except Exception:
            logging.error("Error occured  while converting model to dict")
            raise FieldError("Error occured  while converting model to dict")
