"""
Model for organization
"""
from rest_framework import serializers
from .base_model import BaseModel, models
from uuid import uuid4


class Organization(BaseModel):
    """
    Organization class
    """

    deleted_at = None

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    street_1 = models.TextField()
    street_2 = models.TextField(null=True)
    city = models.TextField()
    county = models.TextField(null=True)
    state = models.TextField()
    country = models.TextField()
    postal_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        db_table = "organizations"


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for Organization model class
    """

    class Meta:
        model = Organization
        fields = "__all__"
