from django.db import models
from ..models import User
from django.utils.timezone import now, timedelta
from django.db import models
from .managers import TotpManager, MFAJoinTokenManager


class Totp(models.Model):
    STATUS_CHOICES = (
        ('initialized', 'Initialized'),
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
        ('backup_used', 'Backup Used')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.BinaryField()
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default='initialized')
    backup_codes = models.BinaryField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    bc_attempts = models.IntegerField(default=0)
    bc_timeout = models.DateTimeField(null=True, blank=True)

    objects = TotpManager()

    def __str__(self):
        return f"{self.user}"


class MFAJoinToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True, blank=True)
    ua = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    # Token expires in 10 minutes
    expire_at = models.DateTimeField(default=now()+timedelta(minutes=10))

    objects = MFAJoinTokenManager()

    def __str__(self):
        return f"{self.user}"
