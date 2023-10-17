from django.forms import CharField
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.utils import timezone

from .serializers import (
    UserRegisterationSerializer,
    UserSerializer,
    PasswordChangeSerializer,
)

from .schema_objects import invalid_register_object, invalid_password_object

__all__ = ["RegisterUserView", "GetOrUpdateUserDataView", "ChangePasswordView"]

User = get_user_model()


@extend_schema(
    description="Takes the user object and create a new user if the user object is valid else raise exceptions",
    tags=["users"],
    request=UserRegisterationSerializer,
    responses={
        status.HTTP_201_CREATED: UserRegisterationSerializer,
        status.HTTP_406_NOT_ACCEPTABLE: UserRegisterationSerializer,
    },
    examples=[
        OpenApiExample(
            name="INVALID_REGISTER",
            status_codes=[status.HTTP_406_NOT_ACCEPTABLE],
            value=invalid_register_object,
            response_only=True,
        )
    ],
)
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
            )


@extend_schema(
    description="Get or patch user by id",
    tags=["users"],
    responses={
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_404_NOT_FOUND: inline_serializer(
            name="NotFound", fields={"phone_number": serializers.CharField()}
        ),
    },
    examples=[
        OpenApiExample(
            name="NOT_FOUND",
            response_only=True,
            status_codes=[status.HTTP_404_NOT_FOUND],
            value={"detail": "Not found."},
        )
    ],
)
class GetOrUpdateUserDataView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):
        user_id = self.kwargs["id"]
        return get_object_or_404(User, pk=user_id)


@extend_schema(
    description="Takes the old password, new password and confirm new password to change the user password.",
    tags=["users"],
    request=PasswordChangeSerializer,
    responses={
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name="InvalidChangePasswordSerializer",
            fields={
                "password": serializers.CharField(max_length=132),
                "new_password": serializers.CharField(max_length=132),
            },
        ),
    },
    examples=[
        OpenApiExample(
            name="INVALID_CHANGE_PASSWORD",
            response_only=True,
            status_codes=[status.HTTP_400_BAD_REQUEST],
            value=invalid_password_object,
        ),
    ],
)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=self.request.user.pk)
        password = self.request.data.get("password")
        new_password = self.request.data.get("new_password")
        if not user.check_password(password):
            return Response(
                data={"password": ["Invalid password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.set_password(new_password)
            user.last_password_change = timezone.now()
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
            )
