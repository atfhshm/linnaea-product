from rest_framework import serializers

from apps.tickets.models import Ticket, TicketComment


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "ticket_type", "status", "content", "created_at", "updated_at")


class TicketCommentSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = TicketComment
        fields = ("id", "ticket", "comment", "created_by", "created_at")
        read_only_fields = ("created_by",)


class TicketsWithCommentsSerializer(serializers.ModelSerializer):
    ticket_comments = TicketCommentSerializer(many=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "ticket_type",
            "content",
            "status",
            "created_at",
            "updated_at",
            "ticket_comments",
        )
        read_only_fields = ["ticket_comments"]
