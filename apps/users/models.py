from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator

from dateutil.relativedelta import relativedelta


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

    def password_reset_required(self):
        return self.last_password_change >= relativedelta(months=3) + timezone.now()
