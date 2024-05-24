from ..users_sessions.utils import get_active_session
from ..users_app_tokens.utils import get_active_token


def get_active_user(request):
    """
    Get the active user from the request

    Args:
        request: HttpRequest

    Returns: User
    """
    session = get_active_session(request)
    if session:
        return session.user
    token = get_active_token(request)
    if token:
        return token.user
    return None
