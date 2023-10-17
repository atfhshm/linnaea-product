from django.urls import path
from .views import TokenPairObtainView, TokenRefreshObtainView

urlpatterns = [
    path("tokens/", TokenPairObtainView.as_view(), name="get-tokens"),
    path("tokens/refresh/", TokenRefreshObtainView.as_view(), name="refresh-token"),
]
