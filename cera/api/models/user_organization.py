"""
Model for organization
"""
from rest_framework import serializers
from .base_model import BaseModel, models
from uuid import uuid4


class UserOrganization(BaseModel):
    """
    Organization class
    """

    deleted_at = None

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    user = models.ForeignKey(
        "User", related_name="organizations", on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        "Organization",
        related_name="users",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "user_organizations"


class UserOrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for Organization model class
    """

    class Meta:
        model = UserOrganization
        fields = "__all__"
