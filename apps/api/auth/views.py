from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenRefreshView

from django.contrib.auth import authenticate
from django.utils import timezone

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample

from apps.users.models import User
from dateutil.relativedelta import relativedelta
from .serializers import (
    TokenObtainPairSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
)

__all__ = ["TokenPairObtainView", "TokenRefreshObtainView"]


@extend_schema(
    description="Takes a set of user credentials and returns a user object with an access and refresh JSON web token pair.",
    tags=["auth"],
    request=TokenObtainPairSerializer,
    responses={
        status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name="InvalidCredentials",
            fields={"detail": serializers.CharField(max_length=128)},
        ),
    },
    examples=[
        OpenApiExample(
            "INVALID_CREDENTIALS",
            value={"detail": "email doesn't exist."},
            status_codes=[401],
            response_only=True,
        )
    ],
)
class TokenPairObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        login = request.data.get("login")
        password = request.data.get("password")
        email_exists = User.objects.filter(email=login).exists()
        if not email_exists:
            return Response(
                data={"detail": "email doesn't exist."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user = authenticate(request, email=login, password=password)
        if user:
            password_reset_required = (
                user.last_password_change >= relativedelta(months=3) + timezone.now()
            )
            if password_reset_required:
                return Response(
                    data="redirect to reset password", status=status.HTTP_303_SEE_OTHER
                )
            user.last_login = timezone.now()
            user.save()
            serializer = TokenObtainPairResponseSerializer(instance=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"detail": "Incorrect password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@extend_schema(
    tags=["auth"],
    responses={
        status.HTTP_200_OK: TokenRefreshResponseSerializer,
        status.HTTP_406_NOT_ACCEPTABLE: inline_serializer(
            name="InvalidToken",
            fields={
                "detail": serializers.CharField(max_length=30),
                "code": serializers.CharField(max_length=30),
            },
        ),
    },
    examples=[
        OpenApiExample(
            name="INVALID_TOKEN",
            status_codes=[status.HTTP_406_NOT_ACCEPTABLE],
            value={"detail": "Token is invalid or expired", "code": "token_not_valid"},
        ),
    ],
)
class TokenRefreshObtainView(TokenRefreshView):
    permission_classes = [AllowAny]
