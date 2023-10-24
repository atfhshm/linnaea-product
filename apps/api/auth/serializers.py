from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

__all__ = [
    "TokenObtainPairSerializer",
    "TokenObtainPairResponseSerializer",
    "TokenRefreshResponseSerializer",
]

User = get_user_model()


class TokenObtainPairSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class TokensSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=132)
    refresh = serializers.CharField(max_length=132)


class TokenObtainPairResponseSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    password_reset_required = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password_reset_required",
            "tokens",
        )

    def get_tokens(self, obj) -> TokensSerializer:
        refresh = RefreshToken.for_user(obj)
        access = refresh.access_token

        return {"access": str(access), "refresh": str(refresh)}

    def get_password_reset_required(self, obj: User) -> bool:
        return obj.password_reset_required


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
