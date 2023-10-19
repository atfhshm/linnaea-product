from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.api.auth.urls")),
    path("users/", include("apps.api.users.urls")),
    path("tickets/", include("apps.api.tickets.urls")),
]
