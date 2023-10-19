from django.urls import path

from .views import (
    CreateTicketView,
    RetrieveTickerWithCommentsView,
    CreateTicketCommentView,
    ListTicketsView,
)

urlpatterns = [
    path("", CreateTicketView.as_view(), name="create-ticket"),
    path("user", ListTicketsView.as_view(), name="list-user-tickets"),
    path(
        "<int:id>",
        RetrieveTickerWithCommentsView.as_view(),
        name="retrieve-tickets-with-comments",
    ),
    path("comments", CreateTicketCommentView.as_view(), name="create-ticket-comment"),
]
