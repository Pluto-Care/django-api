import uuid
from django.db import models
from ..models import User
from django.utils.timezone import now
from django.db import models
from .managers import AppTokenManager


class AppToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    is_valid = models.BooleanField(default=True)
    ip = models.GenericIPAddressField()
    ua = models.TextField()
    created_at = models.DateTimeField(default=now)

    objects = AppTokenManager()

    def __str__(self):
        return f"{self.pk}"
