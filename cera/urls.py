"""cera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
import oauth2_provider.views as oauth2_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from oauth2_provider import views as oauth2_views
from django.urls import re_path

from cera.api.views import (
    UserView,
    TokenApiView,
    UserIdentityView,
    OrganizationCreateGetView,
    OrganizationUpdateView,
    OrganizationUserCreateGetView,
    OrganizationUserUpdateView,
    OrganizationRoleView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path(
        "authorize/",
        oauth2_views.AuthorizationView.as_view(),
        name="authorize",
    ),
    path("token/", TokenApiView.as_view(), name="token"),
    path(
        "revoke-token/",
        oauth2_views.RevokeTokenView.as_view(),
        name="revoke-token",
    ),
]

# This is copied exactly from site-packages/outh2-provider/urls.py
# Because we have to show the openapi doc for /o/token api and we
# created our own custom TokenApiView in oauth2_endpoint_views.
# Not to be touched.
oauth2_management_urlpatterns = [
    # Application management views
    re_path(
        r"^applications", oauth2_views.ApplicationList.as_view(), name="list"
    ),
    re_path(
        r"^applications/register/$",
        oauth2_views.ApplicationRegistration.as_view(),
        name="register",
    ),
    re_path(
        r"^applications/(?P<pk>[\w-]+)/$",
        oauth2_views.ApplicationDetail.as_view(),
        name="detail",
    ),
    re_path(
        r"^applications/(?P<pk>[\w-]+)/delete/$",
        oauth2_views.ApplicationDelete.as_view(),
        name="delete",
    ),
    re_path(
        r"^applications/(?P<pk>[\w-]+)/update/$",
        oauth2_views.ApplicationUpdate.as_view(),
        name="update",
    ),
    # Token management views
    re_path(
        r"^authorized_tokens/$",
        oauth2_views.AuthorizedTokensListView.as_view(),
        name="authorized-token-list",
    ),
    re_path(
        r"^authorized_tokens/(?P<pk>[\w-]+)/delete/$",
        oauth2_views.AuthorizedTokenDeleteView.as_view(),
        name="authorized-token-delete",
    ),
]


urlpatterns = [
    path("me", UserIdentityView.as_view(), name="identity"),
    path("user", UserView.as_view(), name="user_view"),
    path(
        "organization",
        OrganizationCreateGetView.as_view(),
        name="organization_create_get_view",
    ),
    path(
        "organization/<str:pk>",
        OrganizationUpdateView.as_view(),
        name="organization_update_view",
    ),
    path(
        "organization_role",
        OrganizationRoleView.as_view(),
        name="organization_role_view",
    ),
    path(
        "organization/<str:pk>/user",
        OrganizationUserCreateGetView.as_view(),
        name="organization_user_create_get_view",
    ),
    path(
        "organization/<str:org_pk>/user/<str:user_pk>",
        OrganizationUserUpdateView.as_view(),
        name="organization_user_update_view",
    ),
    path("admin", admin.site.urls),
    path(
        "o/",
        include(
            (
                oauth2_endpoint_views + oauth2_management_urlpatterns,
                "oauth2_provider",
            ),
            namespace="oauth2_provider",
        ),
    ),
    # path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path(
        "swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
