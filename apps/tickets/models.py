from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class TicketTypeChoices(models.TextChoices):
    TECHNICAL = "TECHNICAL", "Technical"
    GENERAL = "GENERAL", "General"
    OTHER = "OTHER", "Other"


class StatusChoices(models.TextChoices):
    OPEN = "OPENED", "Opened"
    RESOLVED = "RESOLVED", "Resolved"


class Ticket(models.Model):
    content = models.TextField(_("ticket content"))
    ticket_type = models.CharField(
        _("ticket type"),
        choices=TicketTypeChoices.choices,
        default=TicketTypeChoices.TECHNICAL,
    )
    status = models.CharField(
        _("ticket status"), choices=StatusChoices.choices, default=StatusChoices.OPEN
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tickets",
        null=True,
        blank=True,
    )
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submitted_tickets"
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "tickets"
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.pk!s}"


class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name=_("ticket_comments"),
        verbose_name=_("ticket"),
    )
    comment = models.TextField(_("comment"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_comments",
        verbose_name=_("comment creator"),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        db_table = "ticket_comments"
        verbose_name = _("ticket comment")
        verbose_name_plural = _("ticket comments")
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.pk!s}"
