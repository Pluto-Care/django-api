import json
from django.db import models
from users.users_sessions.utils import get_active_session
from users.users_app_tokens.utils import get_active_token


class LogManager(models.Manager):
    def __init__(self):
        super().__init__()

    def create_log(self, request, response):
        """Create a Log entry in the database

        Args:
            request: HTTP request object
            response (dict): Response in format of LogResponse.serialize()
            user (User, optional): User who is performing the action. Defaults to logged-in user or None.
        """
        status = response['s']
        response.pop('s', None)
        session = get_active_session(request)
        app_token = get_active_token(request)
        log = self.model(
            url=request.get_full_path(),
            status=status,
            context=json.dumps(response['m'] if hasattr(
                response, 'm') else response),
            session=session.id if session is not None else None,
            app_token=app_token.id if app_token is not None else None,
            ip=getClientIP(request),
            ua=getUserAgent(request)
        )
        log.save()


# Get Client IP Address
def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Get User Agent
def getUserAgent(request):
    return request.META.get('HTTP_USER_AGENT')
