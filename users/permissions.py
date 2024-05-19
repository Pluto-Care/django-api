from rest_framework import permissions
from .users_sessions.utils import get_active_session
from .users_app_tokens.utils import get_active_token


class HasSessionActive(permissions.BasePermission):
    message = 'Unauthorized!'
    """
    Permission to check if user session is present
    """

    def has_permission(self, request, view):
        session = get_active_session(request)
        return True if session and session.user.is_active else False


class HasTokenActive(permissions.BasePermission):
    message = 'Unauthorized!'
    """
    Permission to check if user session is present
    """

    def has_permission(self, request, view):
        session = get_active_token(request)
        return True if session and session.user.is_active else False


class HasSessionOrTokenActive(permissions.BasePermission):
    message = 'Unauthorized!'
    """
    Permission to check if user session is present
    """

    def has_permission(self, request, view):
        session = get_active_session(request)
        token = get_active_token(request)
        return True if (session and session.user.is_active) or (token and token.user.is_active) else False
