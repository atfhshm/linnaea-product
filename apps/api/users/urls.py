from django.urls import path
from .views import RegisterUserView, GetOrUpdateUserDataView, ChangePasswordView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register-user"),
    path("<int:id>/", GetOrUpdateUserDataView.as_view(), name="get-patch-user"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
