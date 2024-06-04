import json
from django.db import models
from django.utils.timezone import now
from .managers import LogManager
from users.users_app_tokens.api import get_user as get_user_from_app_token
from users.users_sessions.api import get_user as get_user_from_session


class ApiCallLog(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
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

    class Meta:
        verbose_name = 'API Call Log'
        verbose_name_plural = 'API Call Logs'
        ordering = ('-created_at',)

    @property
    def user_email(self):
        if self.app_token:
            user = get_user_from_app_token(self.app_token)
            if user:
                return user.email
        elif self.session:
            user = get_user_from_session(self.session)
            if user:
                return user.email
        else:
            context = json.loads(self.context)
            if 'm' in context and 'user' in context['m']:
                """This only works for login and sign up requests as the APILogMiddleware
                the user object and store it in log context"""
                return context['m']['user']
        return None

    def __str__(self):
        return 'ID: ' + str(self.pk)
