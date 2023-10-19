from django.contrib import admin

from .models import Ticket, TicketComment


@admin.register(Ticket)
class TicketAdminCongif(admin.ModelAdmin):
    list_display = (
        "id",
        "submitted_by",
        "ticket_type",
        "status",
        "created_at",
        "assigned_to",
    )


@admin.register(TicketComment)
class TicketCommentAdminConfig(admin.ModelAdmin):
    list_display = (
        "id",
        "ticket",
        "created_by",
        "created_at"
    )
