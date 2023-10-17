from rest_framework import serializers
from rest_framework import status

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


__all__ = ["UserRegisterationSerializer", "UserSerializer"]


class UserRegisterationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=32, write_only=True)

    class Meta:
        model = User

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "password",
            "confirm_password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attr: dict):
        password = attr.get("password")
        confirm_password = attr.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                detail={"password": ["Passwords missmatch."]},
                code=status.HTTP_400_BAD_REQUEST,
            )
        return attr

    def validate_password(self, value: str):
        if value:
            validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        user = User.objects.create(
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            phone_number=validated_data.get("phone_number"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "username", "phone_number")
        read_only_fields = ("id", "first_name", "last_name", "email", "username")


class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=32)
    new_password = serializers.CharField(max_length=32)
    confirm_password = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = ("password", "new_password", "confirm_password")
        read_only_fields = ("new_password", "confirm_password")

    def validate(self, attrs: dict):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError(
                detail={"new_password": ["Passwords missmatch."]},
                code=status.HTTP_400_BAD_REQUEST,
            )

        return attrs

    def validate_new_password(self, value):
        if value:
            validate_password(value)
        return value
