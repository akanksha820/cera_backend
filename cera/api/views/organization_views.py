"""
Views for me endpoint
"""
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.views import APIView
from oauth2_provider.views.generic import ProtectedResourceView
from drf_yasg.utils import swagger_auto_schema

from cera.api.models import User, Organization, OrganizationSerializer


class OrganizationView(ProtectedResourceView, APIView):
    """
    Class for /me
    """

    @swagger_auto_schema(
        operation_description="Get all organizations",
        responses={200: OrganizationSerializer(many=True)},
    )
    def get(self, request):
        user = User.objects.get(pk=request.user.id)

        if user is None:
            raise User.DoesNotExist

        if not user.has_perm("api.view_organization"):
            return HttpResponseForbidden()

        organizations = Organization.objects.all()

        serializer = OrganizationSerializer(organizations, many=True)
        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        operation_description="Create a new organization",
        responses={200: OrganizationSerializer(many=True)},
        request_body=OrganizationSerializer(),
    )
    def post(self, request):
        user = User.objects.get(pk=request.user.id)

        if user is None:
            raise User.DoesNotExist

        if not user.has_perm("api.create_organization"):
            return HttpResponseForbidden()

        serializer = OrganizationSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors)

        serializer.save()

        return JsonResponse(serializer.data)