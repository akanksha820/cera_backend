"""
Views for organization users endpoint
"""
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from oauth2_provider.views.generic import ProtectedResourceView
from drf_yasg.utils import swagger_auto_schema
from cera.api.models import (
    User,
    UserSerializer,
    Organization,
    UserOrganization,
    UserOrganizationSerializer,
    OrganizationUserSerializer,
    Role,
)
from cera.api.utils import UserNotInOrgException

import logging

logger = logging.getLogger(__name__)


class OrganizationUserCreateGetView(ProtectedResourceView, APIView):
    """
    Class for /organization/<pk>
    """

    @swagger_auto_schema(
        operation_description="Get the authenticated user's details",
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request, **kwargs):
        organization_id = kwargs["pk"]

        try:
            organization = Organization.objects.get(pk=organization_id)

            if not organization:
                raise Organization.DoesNotExist

            org_users = organization.users.all()

            users = []
            for org_user in org_users:
                user = org_user.user
                user.role = org_user.role
                users.append(user)

            serializer = OrganizationUserSerializer(users, many=True)

            return JsonResponse(serializer.data, safe=False)
        except ObjectDoesNotExist as ex:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "Org not found"}, status=HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            logger.exception(ex)
            return JsonResponse(
                {"detail": e.messages}, status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "Internal Error"}, safe=False, status=500
            )

    @swagger_auto_schema(
        operation_description="Get the authenticated user's details",
        responses={200: UserSerializer()},
    )
    def post(self, request, **kwargs):
        organization_id = kwargs["pk"]

        try:
            organization = Organization.objects.get(pk=organization_id)

            if not organization:
                raise Organization.DoesNotExist

            user = User.objects.get(pk=request.user.id)

            if user is None:
                raise User.DoesNotExist

            # if not user.has_perm("api.add_user"):
            #     return HttpResponseForbidden()

            serializer = OrganizationUserSerializer(data=request.data)

            if not serializer.is_valid():
                return JsonResponse(serializer.errors)

            serializer.save(organization=organization)

            return JsonResponse(serializer.data)

        except Organization.DoesNotExist:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "Org not found"}, status=HTTP_400_BAD_REQUEST
            )
        except Role.DoesNotExist:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "Role not found"}, status=HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "User not found"}, status=HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            logger.exception(ex)
            return JsonResponse(
                {"detail": e.messages}, status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "Internal Error"},
                safe=False,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OrganizationUserUpdateView(ProtectedResourceView, APIView):
    """
    Class for /organization/<org_pk>/<user_pk>
    """

    @swagger_auto_schema(
        operation_description="Get the authenticated user's details",
        responses={200: UserSerializer()},
        request_body=UserSerializer(),
    )
    def put(self, request, **kwargs):
        organization_id = kwargs["org_pk"]

        user_id = kwargs["user_pk"]

        try:
            organization = Organization.objects.get(pk=organization_id)

            if not organization:
                raise Organization.DoesNotExist

            auth_user = User.objects.get(pk=request.user.id)

            if auth_user is None:
                raise User.DoesNotExist

            # Should be checked if the user has permission to add user or
            # for only one's own organization
            # if not auth_user.has_perm("api.add_user"):
            #     return HttpResponseForbidden()

            user = User.objects.get(pk=user_id)

            # This is not needed as we are saving first and roles
            # is set to user there
            # user.role = user_org[0].role

            serializer = OrganizationUserSerializer(user, data=request.data)

            if not serializer.is_valid():
                return JsonResponse(serializer.errors)

            serializer.save(organization=organization)

            return JsonResponse(serializer.data)

        except Organization.DoesNotExist:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "Org not found"}, status=HTTP_400_BAD_REQUEST
            )
        except Role.DoesNotExist:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "Role not found"}, status=HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "User not found"}, status=HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            logger.exception(ex)
            return JsonResponse(
                {"detail": e.messages}, status=HTTP_400_BAD_REQUEST
            )
        except UserNotInOrgException as e:
            logger.exception(ex)
            return JsonResponse(
                {"detail": e.message}, status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(ex)
            return JsonResponse(
                {"detail": "Internal Error"},
                safe=False,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
