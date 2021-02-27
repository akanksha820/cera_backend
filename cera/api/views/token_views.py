"""
Views for token api
"""

from oauth2_provider.views.base import TokenView
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


token_response = openapi.Response(
    "response description",
    openapi.Schema(
        title="Token response",
        type=openapi.TYPE_OBJECT,
        properties={
            "access_token": openapi.Schema(
                title="access_token", type=openapi.TYPE_STRING
            ),
            "expires_in": openapi.Schema(
                title="expires_in", type=openapi.TYPE_INTEGER
            ),
            "token_type": openapi.Schema(
                title="token_type", type=openapi.TYPE_STRING
            ),
            "scope": openapi.Schema(title="scope", type=openapi.TYPE_STRING),
            "refresh_token": openapi.Schema(
                title="refresh_token", type=openapi.TYPE_STRING
            ),
        },
    ),
)

token_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING, description="string"
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING, description="string"
        ),
        "client_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="string"
        ),
        "client_secret": openapi.Schema(
            type=openapi.TYPE_STRING, description="string"
        ),
        "grant_type": openapi.Schema(
            type=openapi.TYPE_STRING, description="string"
        ),
    },
)


class TokenApiView(TokenView, APIView):
    """
    Class for /token api
    """

    # Need to find out how to set the schema of request form body
    @swagger_auto_schema(
        responses={200: token_response}, request_body=token_body
    )
    def post(self, request, *args, **kwargs):
        """
        Create an oauth2 token
        """
        return super().post(request, *args, **kwargs)
