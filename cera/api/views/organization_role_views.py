"""
Views for organization roles endpoint
"""
from django.http import JsonResponse
from rest_framework.views import APIView
from oauth2_provider.views.generic import ProtectedResourceView
from drf_yasg.utils import swagger_auto_schema

from cera.api.models import Role, RoleSerializer, OrganizationTypeEnum


class OrganizationRoleView(ProtectedResourceView, APIView):
    """
    Class for /organization_role
    """

    @swagger_auto_schema(
        operation_description="Get the authenticated user's details",
        responses={200: RoleSerializer(many=True)},
    )
    def get(self, request):
        roles = Role.objects.filter(
            organization_type=OrganizationTypeEnum.SCHOOL
        )
        serializer = RoleSerializer(roles, many=True)
        return JsonResponse(serializer.data, safe=False)