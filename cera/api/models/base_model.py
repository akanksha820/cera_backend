from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField("created at", auto_now_add=True)
    updated_at = models.DateTimeField("updated at", auto_now=True)
    deleted_at = models.DateTimeField("deleted at", null=True)

    class Meta:
        abstract = True