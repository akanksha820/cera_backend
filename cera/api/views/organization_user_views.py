"""
Views for me endpoint
"""
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.views import APIView
from oauth2_provider.views.generic import ProtectedResourceView
from drf_yasg.utils import swagger_auto_schema

from cera.api.models import (
    User,
    UserSerializer,
    Organization,
    UserOrganization,
    UserOrganizationSerializer,
)

import sys


class OrganizationUserView(ProtectedResourceView, APIView):
    """
    Class for /me
    """

    @swagger_auto_schema(
        operation_description="Get the authenticated user's details",
        responses={200: UserSerializer()},
    )
    def get(self, request, **kwargs):
        organization_id = kwargs["pk"]

        try:
            organization = Organization.objects.get(pk=organization_id)

            if not organization:
                raise Organization.DoesNotExist

            org_users = organization.users.all()

            serializer = UserSerializer(
                [org_user.user for org_user in org_users], many=True
            )

            return JsonResponse(serializer.data, safe=False)
        except Organization.DoesNotExist:
            return JsonResponse({"detail": "Org not found"}, status=400)
        except ValidationError as e:
            return JsonResponse({"detail": e.messages}, status=400)
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
            print(str(e))
            return JsonResponse(
                {"detail": "Internal Error"}, safe=False, status=500
            )

    def post(self, request, **kwargs):
        organization_id = kwargs["pk"]

        organization = Organization.objects.get(pk=organization_id)

        if not organization:
            raise Organization.DoesNotExist

        user = User.objects.get(pk=request.user.id)

        if user is None:
            raise User.DoesNotExist

        if not user.has_perm("api.add_user"):
            return HttpResponseForbidden()

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors)

        with transaction.atomic():

            db_user = serializer.save()

            user_organization = UserOrganization.objects.create(
                user=db_user, organization=organization
            )

            organization.users.add(user_organization)

        return JsonResponse(serializer.data)