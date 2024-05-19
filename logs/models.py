from django.db import models
from django.utils.timezone import now
from .managers import LogManager


class ApiCallLog(models.Model):
    # API URL that the user is trying to access
    url = models.CharField(max_length=255)
    # Response brief for success or error
    # Example: {"status": 200, "message": "Success"}
    # Use LogResponse.serialize() to serialize useful information
    context = models.JSONField(null=True, blank=True)
    # Active session when user is performing the action
    # For login and signup, session_id is None. Instead,
    # 'context' column will have 'user' key.
    session = models.UUIDField(null=True, blank=True)
    app_token = models.UUIDField(null=True, blank=True)
    status = models.IntegerField()
    ip = models.GenericIPAddressField(null=True, blank=True)
    ua = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    objects = LogManager()

    def __str__(self):
        return 'ID ' + str(self.pk)
