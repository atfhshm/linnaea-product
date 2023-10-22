from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import User, Token

admin.site.register(Permission)


@admin.register(User)
class UserAdminConfig(UserAdmin):
    fieldsets = (
        (
            "basic info",
            {
                "fields": (
                    "email",
                    "phone_number",
                    "role",
                    "password",
                )
            },
        ),
        (
            "personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
    )

    list_display = (
        "id",
        "email",
        "phone_number",
        "date_joined",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "last_password_change",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "role",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    list_filter = ("is_active", "is_staff", "is_superuser", "role")
    search_fields = ("phone_number", "email")
    ordering = ("id", "email")


@admin.register(Token)
class TokenAdminConfig(admin.ModelAdmin):
    list_display = ["id", "token", "user", "created_at", "expired_at", "is_used"]
