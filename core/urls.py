from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls"), name="api-urls"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="schema-docs",
    ),
]

if settings.DEBUG:
    urlpatterns.extend(
        urlpattern
        for urlpattern in (
            # the * start before static is used for sequence unpacking
            # because static returns a list of urlpatterns
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        )
    )
