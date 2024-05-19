from calendar import c
from django.db import models
from .utils import generateKey, getClientIP, getUserAgent, hash_this
from users.api import get_user


class ForgotPasswordManager(models.Manager):
    def __init__(self):
        super().__init__()

    def create_forgot_password(self, request, email):
        user = get_user(email)
        if not user:
            return None, None
        # create forgot password instance
        key = generateKey()
        fp = self.create(
            user=user,
            key=hash_this(key),
            ip=getClientIP(request),
            ua=getUserAgent(request)
        )
        return key, fp
