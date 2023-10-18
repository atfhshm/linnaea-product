from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from dateutil.relativedelta import relativedelta
from datetime import timedelta

from secrets import token_urlsafe


class RoleChoices(models.TextChoices):
    ORG_ADMIN = "ORG_ADMIN", "organization admin"
    ORG_MANAGER = "ORG_MANAGER", "organization managers"
    ORG_MEMBER = "ORG_MEMBERS", "organization member"
    INTERNAL = "INTERNAL", "internal"


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email must be provided")
        if not extra_fields.get("phone_number", None):
            raise ValueError("phone number must be provided")
        email = self.normalize_email(email=email)
        user: User = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        _("first name"), max_length=150, null=False, blank=False
    )
    last_name = models.CharField(
        _("last name"), max_length=150, null=False, blank=False
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=20,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    role = models.CharField(
        _("role"),
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.INTERNAL,
    )
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("created at"), default=timezone.now)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    last_password_change = models.DateTimeField(
        _("last password change"),
        editable=False,
        default=timezone.now,
    )
    phone_verified = models.BooleanField(_("verified phone"), default=False)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number", "first_name", "last_name"]

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return f"{self.email}"

    @property
    def password_reset_required(self):
        return self.last_password_change + relativedelta(months=3) <= timezone.now()


class Token(models.Model):
    token = models.CharField(
        _("token"), max_length=6, unique=True, db_index=True, editable=False
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="user_tokens",
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    expired_at = models.DateTimeField(_("expired_at"), editable=False)
    is_used = models.BooleanField(_("is used"), default=False)

    class Meta:
        db_table = "tokens"
        verbose_name = _("token")
        verbose_name_plural = _("tokens")

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.token = self.generate_token()
            self.expired_at = timezone.now() + timedelta(
                seconds=settings.TOKEN_EXPIRY_SECONDS
            )
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.token}"

    def generate_token(self):
        return token_urlsafe(4)

    @property
    def is_valid(self):
        return timezone.now() <= self.expired_at

    def remove_expired_tokens(self) -> None:
        Token.objects.filter(user=self.user, expired_at__lte=timezone.now()).delete()
