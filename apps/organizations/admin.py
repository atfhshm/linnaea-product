from django.contrib import admin

from .models import (
    Organization,
    OrganizationInvitation,
    OrganizationMember,
    OrganizationBranch,
    BranchMember,
)


@admin.register(Organization)
class OrganizationAdminConfig(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "status", "user", "created_at", "updated_at"]


@admin.register(OrganizationInvitation)
class OrganizationInvitationAdminConfig(admin.ModelAdmin):
    list_display = [
        "id",
        "token",
        "organization",
        "email",
        "created_at",
        "expired_at",
        "valid",
    ]

    def valid(self, obj) -> bool:
        return obj.valid

    valid.boolean = True


@admin.register(OrganizationMember)
class OrganizationMemberAdminConfig(admin.ModelAdmin):
    list_display = [
        "id",
        "organization",
        "user",
        "is_active",
        "created_at",
        "updated_at",
    ]


# TODO: ADD AdminConfig
admin.site.register([OrganizationBranch, BranchMember])
