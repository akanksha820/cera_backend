"""
Views for me endpoint
"""
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.views import APIView
from oauth2_provider.views.generic import ProtectedResourceView
from drf_yasg.utils import swagger_auto_schema

from cera.api.models import User, UserSerializer


class UserView(ProtectedResourceView, APIView):
    """
    Class for /me
    """

    @swagger_auto_schema(
        operation_description="Get the authenticated user's details",
        responses={200: UserSerializer()},
    )
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        user = User.objects.get(pk=request.user.id)

        if user is None:
            raise User.DoesNotExist

        if not user.has_perm("api.add_user"):
            return HttpResponseForbidden()

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors)

        serializer.save()

        return JsonResponse(serializer.data)