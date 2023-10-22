import secrets
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.conf import settings

User = get_user_model()


class Organization(models.Model):
    class OrganizationStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"

    name = models.CharField(_("organization name"), max_length=64)
    slug = models.SlugField(
        _("organization slug"), max_length=84, unique=True, editable=False
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("organization owner")
    )
    status = models.CharField(
        _("organization status"),
        choices=OrganizationStatus.choices,
        default=OrganizationStatus.ACTIVE,
        db_index=True,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "organizations"
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
        indexes = [models.Index(fields=("slug", "status"))]

    def __str__(self) -> str:
        return f"{self.name!s}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name + " " + secrets.token_hex(2))
        return super().save(*args, **kwargs)


class OrganizationInvitation(models.Model):
    token = models.UUIDField(
        _("invitation token"), default=uuid4, unique=True, editable=False
    )
    email = models.EmailField(_("invited email"))
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="org_invitations",
        verbose_name=_("Organization invitations"),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    expired_at = models.DateTimeField(_("expired at"), editable=False)

    class Meta:
        db_table = "org_invitations"
        verbose_name = "Organization Invitation"
        verbose_name_plural = "Organization Invitation"

    def __str__(self) -> str:
        return f"{self.token!s}"

    def save(self, *args, **kwargs):
        if not self.pk:
            expiry_duration = settings.INVITATION_EXPIRY_SECONDS
            self.expired_at = timezone.now() + relativedelta(seconds=expiry_duration)
        return super().save(*args, **kwargs)

    @property
    def valid(self) -> bool:
        return timezone.now() <= self.expired_at


class OrganizationMember(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="org_members"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    is_active = models.BooleanField(_("member status"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "org_members"
        verbose_name = _("organization member")

    def __str__(self) -> str:
        return f"{self.organization}: {self.user}"


# id int [pk, not null, increment]
#   name varchar(32)
#   slug varchar(64) [unique]
#   organization int [ref: > organizations.id]
#   created_at datetime [default: `NOW()`]
#   updated_at datetime


class OrganizationBranch(models.Model):
    name = models.CharField(_("organization name"), max_length=64)
    slug = models.SlugField(
        _("organization slug"), max_length=84, unique=True, editable=False
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name=_("organization")
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "org_branches"
        verbose_name = _("organization branch")
        verbose_name_plural = _("organization branches")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name + " " + secrets.token_hex(2))
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name!s}"


class BranchMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    branch = models.ForeignKey(
        OrganizationBranch,
        on_delete=models.CASCADE,
        related_name="branch_members",
        verbose_name=_("branch"),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "branch_members"
        verbose_name = _("branch member")
        verbose_name_plural = _("branch members")

    def __str__(self) -> str:
        return f"{self.branch}: {self.user}"
