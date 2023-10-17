from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import User

admin.site.register(Permission)


@admin.register(User)
class UserAdminConfig(UserAdmin):
    fieldsets = (
        (
            "basic info",
            {"fields": ("email", "username", "phone_number", "password")},
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
        "username",
        "date_joined",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
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
                    "username",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )

    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("phone_number", "email", "username")
    ordering = ("id", "email")
