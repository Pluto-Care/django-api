##########################################################
#
#                   Outward facing API
#
# This file should ideally be the only export from this
# module/app. (Except permissions.py, middlewares.py)
#
# Using imports from other files may breach security.
#
# If you need to use any other function from this package,
# consider making a new function here and calling that.
#
##########################################################

from .models import Session
from .serializers import SessionSerializer, UserSessionSerializer


def create_session(user, request) -> tuple[str, Session]:
    """
    Create a new session for the user

    Args:
        user: User
        request: HttpRequest

    Returns: tuple[key, session]
        key: str
        session: Session
    """
    return Session.objects.create_session(user, request)


def delete_session(user, session_id):
    """
    Delete all sessions for the user

    Args:
        user: User
        session_id: int

    Returns: None
    """
    Session.objects.delete_session(user, session_id)


def get_user(session_id):
    """
    Get the user for the session

    Args:
        session_id: int
    """
    return Session.objects.get_user(session_id)


def get_last_session_details(user):
    """
    Get the last session details for the user

    Args:
        user: User
    """
    session = Session.objects.get_last_session(user)
    if session is not None:
        return UserSessionSerializer(session).data
    return session


def get_session_if_valid(user, session_id, serialized=False):
    """
    Get session for the user given the session_id

    Args:
        user: User
        session_id: int
    """
    session = Session.objects.get_session_if_valid(user, session_id)
    if session is not None and serialized:
        return SessionSerializer(session).data
    return session


def get_all_sessions(user, serialized=False):
    sessions = Session.filter(user=user)
    if serialized:
        return SessionSerializer(sessions, many=True).data
    return sessions


def get_all_active_sessions(user, serialized=False):
    sessions = Session.filter(user=user, is_valid=True)
    if serialized:
        return SessionSerializer(sessions, many=True).data
    return sessions


def delete_all_sessions(user):
    Session.filter(user=user, is_valid=True).update(is_valid=False)
    return None


def delete_all_sessions_except(user, session_id):
    Session.filter(user=user, is_valid=True).exclude(
        pk=session_id).update(is_valid=False)
    return None
