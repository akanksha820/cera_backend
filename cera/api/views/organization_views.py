"""
Views for organization endpoint
"""
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.views import APIView
from oauth2_provider.views.generic import ProtectedResourceView
from drf_yasg.utils import swagger_auto_schema

from cera.api.models import User, Organization, OrganizationSerializer


class OrganizationCreateGetView(ProtectedResourceView, APIView):
    """
    Class for /organization
    """

    @swagger_auto_schema(
        operation_description="Get all organizations",
        responses={200: OrganizationSerializer(many=True)},
    )
    def get(self, request):
        user = User.objects.get(pk=request.user.id)

        if user is None:
            raise User.DoesNotExist

        # if not user.has_perm("api.view_organization"):
        #     return HttpResponseForbidden()

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

        # if not user.has_perm("api.create_organization"):
        #     return HttpResponseForbidden()

        serializer = OrganizationSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors)

        serializer.save()

        return JsonResponse(serializer.data)


class OrganizationUpdateView(ProtectedResourceView, APIView):
    """
    Class for /organization/<pk>
    """

    @swagger_auto_schema(
        operation_description="Create a new organization",
        responses={200: OrganizationSerializer(many=True)},
        request_body=OrganizationSerializer(),
    )
    def put(self, request, **kwargs):
        user = User.objects.get(pk=request.user.id)

        if user is None:
            raise User.DoesNotExist

        org_id = kwargs["pk"]

        # if not user.has_perm("api.create_organization"):
        #     return HttpResponseForbidden()

        try:
            organization = Organization.objects.get(pk=org_id)

            serializer = OrganizationSerializer(
                organization, data=request.data
            )

            if not serializer.is_valid():
                return JsonResponse(serializer.errors)

            serializer.save()
        except Organization.DoesNotExist:
            return JsonResponse(
                {"detail": "Org not found"}, status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
            print(str(e))
            return JsonResponse(
                {"detail": "Internal Error"}, safe=False, status=500
            )

        return JsonResponse(serializer.data)