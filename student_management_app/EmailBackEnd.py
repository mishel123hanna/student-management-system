from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model
class EmailBackEnd(ModelBackend):
    def authenticate(self, username: str, password: str , **kwargs: Any):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email = username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None