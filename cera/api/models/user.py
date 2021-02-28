from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from uuid import uuid4

from .base_model import BaseModel
from .role import RoleSerializer, RoleIdSerializer, Role, OrganizationTypeEnum
from .user_organization import UserOrganization

from cera.api.utils import UserNotInOrgException


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not username:
            raise ValueError("The given email must be set")
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class UserGender(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")


class User(AbstractUser, BaseModel):
    email = None
    deleted_at = None
    created_at = None

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.EmailField(unique=True, max_length=255)
    first_name = models.TextField(verbose_name="first name")
    last_name = models.TextField(verbose_name="last name")
    phone = models.TextField(verbose_name="phone number")
    is_archived = models.BooleanField(default=False)
    gender = models.TextField(choices=UserGender.choices)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "api"
        db_table = "users"


class UserSerializer(serializers.ModelSerializer):
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "phone",
            "password",
            "gender",
            "is_archived",
            "is_staff",
            "is_superuser",
        ]
        read_only_fields = ["is_staff", "is_superuser", "is_archived"]
        extra_kwargs = {"password": {"write_only": True}}


class OrganizationUserSerializer(UserSerializer):
    role = RoleIdSerializer()

    @transaction.atomic()
    def create(self, validated_data):
        role_data = validated_data.pop("role")

        role_id = role_data.get("id")

        roles = Role.objects.filter(
            pk=role_id, organization_type=OrganizationTypeEnum.SCHOOL
        )

        if len(roles) == 0:
            raise Role.DoesNotExist

        role = roles[0]

        organization = validated_data.pop("organization")

        user = super().create(validated_data)

        user_organization = UserOrganization.objects.create(
            user=user, organization=organization, role=role
        )

        organization.users.add(user_organization)

        user.role = role

        return user

    @transaction.atomic()
    def update(self, instance, validated_data):
        organization = validated_data.get("organization")

        existing_user_orgs = UserOrganization.objects.filter(
            user=instance, organization=organization
        )

        if len(existing_user_orgs) == 0:
            raise UserNotInOrgException()

        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.phone = validated_data.get("phone", instance.phone)
        instance.is_archived = validated_data.get(
            "is_archived", instance.is_archived
        )
        instance.gender = validated_data.get("gender", instance.gender)

        instance.save()

        request_role = validated_data.get("role")

        if request_role:
            role_id = request_role.get("id")

            roles = Role.objects.filter(
                pk=role_id, organization_type=OrganizationTypeEnum.SCHOOL
            )

            if len(roles) == 0:
                raise Role.DoesNotExist

            new_role = roles[0]

            existing_user_org = existing_user_orgs[0]

            existing_user_org.role = new_role

            existing_user_org.save()

            instance.role = new_role

        return instance

    class Meta(UserSerializer.Meta):
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ["role"]
        read_only_fields = UserSerializer.Meta.read_only_fields
        extra_kwargs = UserSerializer.Meta.extra_kwargs
        depth = 1
