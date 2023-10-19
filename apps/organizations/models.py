from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


# class Organization(models.Model):
#     ...

#     class Meta:
#         db_table = "organizations"
#         verbose_name = _("organization")
#         verbose_name_plural = _("organizations")


# class Branch(models.Model):
#     ...

#     class Meta:
#         db_table = "branches"
#         verbose_name = _("branch")
#         verbose_name_plural = _("branches")


# class Member(models.Model):
#     ...

#     class Meta:
#         db_table = "members"
#         verbose_name = _("member")
#         verbose_name_plural = _("members")
