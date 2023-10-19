from django_filters import FilterSet, OrderingFilter
from apps.tickets.models import Ticket


class TicketFilter(FilterSet):
    o = OrderingFilter(fields=(("created_at", "created_at"),))

    class Meta:
        model = Ticket
        fields = ("status", "ticket_type")
