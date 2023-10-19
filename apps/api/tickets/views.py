from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.api.tickets.serializers import (
    TicketCommentSerializer,
    TicketSerializer,
    TicketsWithCommentsSerializer,
)

from drf_spectacular.utils import extend_schema

from apps.tickets.models import Ticket
from ..utils.pagination import Pagination
from ..utils.filters import TicketFilter

__all__ = [
    "CreateTicketView",
    "RetrieveTickerWithCommentsView",
    "CreateTicketCommentView",
]


@extend_schema(tags=["tickets"])
class ListTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    filterset_class = TicketFilter

    def get_queryset(self):
        return Ticket.objects.filter(submitted_by=self.request.user)


@extend_schema(tags=["tickets"])
class CreateTicketView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


@extend_schema(tags=["tickets"])
class RetrieveTickerWithCommentsView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketsWithCommentsSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "id"
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        return Ticket.objects.prefetch_related("ticket_comments").filter(
            submitted_by=self.request.user
        )


@extend_schema(tags=["tickets"])
class CreateTicketCommentView(generics.CreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
