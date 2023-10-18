from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model, login
from django.http.request import HttpRequest

from django.db.models import Q

UserModel = get_user_model()

__all__ = ["EmailBackend"]


class EmailBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest,
        email: str | None = ...,
        password: str | None = ...,
        **kwargs: Any
    ) -> UserModel | None:
        users = UserModel.objects.filter(email=email)
        if users.exists():
            user = users.first()
            if user.check_password(password):
                login(request=request, user=user, backend="apps.users.auth_backend.EmailBackend")
                return user
        else:
            return None

        def get_user(self, user_id):
            user = UserModel.objects.filter(pk=user_id)
            if user:
                return user.first()
            else:
                return None
