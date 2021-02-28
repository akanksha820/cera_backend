"""
Model for organization
"""
from rest_framework import serializers
from .base_model import BaseModel, models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


class OrganizationTypeEnum(models.TextChoices):
    SCHOOL = "SCHOOL", _("School")
    POLICE_DEPARTMENT = "POLICE_DEPARTMENT", _("Police Department")
    EMS = "EMS", _("Emergency Medical Service")


class Role(BaseModel):
    """
    Organization class
    """

    deleted_at = None

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField()
    organization_type = models.TextField(choices=OrganizationTypeEnum.choices)

    class Meta:
        db_table = "roles"


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for Organization model class
    """

    class Meta:
        model = Role
        fields = "__all__"


class RoleIdSerializer(serializers.ModelSerializer):
    """
    Serializer for Organization model class
    """

    id = serializers.UUIDField()

    class Meta:
        model = Role
        fields = ["id"]
