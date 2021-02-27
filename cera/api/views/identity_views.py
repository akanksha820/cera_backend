"""
Views for me endpoint
"""
from django.http import JsonResponse
from rest_framework.views import APIView
from oauth2_provider.views.generic import ProtectedResourceView
from drf_yasg.utils import swagger_auto_schema

from cera.api.models import User, UserSerializer


class UserIdentityView(ProtectedResourceView, APIView):
    """
    Class for /me
    """

    @swagger_auto_schema(
        operation_description="Get the authenticated user's details",
        responses={200: UserSerializer()},
    )
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)