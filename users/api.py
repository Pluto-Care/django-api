from .models import User
from core.middlewares import is_web
# Session Imports
from .users_sessions.utils import get_active_session
# App Token Imports
from .users_app_tokens.utils import get_active_token


def get_user(email):
    """
    Get active User object

    Args:
        email (str): User email

    Returns: User or None
    """
    try:
        account = User.objects.get(email=email, is_active=True)
        return account
    except User.DoesNotExist:
        return None


def get_request_user(request):
    if is_web(request):
        # Check if session is active
        session = get_active_session(request)
        if session is not None:
            return session.user
    # Check if token is active
    app_token = get_active_token(request)
    if app_token is not None:
        return app_token.user
    return None
