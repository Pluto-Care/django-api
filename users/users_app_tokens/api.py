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

from .models import AppToken
from .serializers import AppTokenSerializer, UserAppTokenSerializer


def create_app_token(user, request) -> tuple[str, AppToken]:
    """
    Create a new app_token for the user

    Args:
        user: User
        request: HttpRequest

    Returns: tuple[key, app_token]
        key: str
        app_token: AppToken
    """
    return AppToken.objects.create_app_token(user, request)


def delete_app_token(user, app_token_id):
    """
    Delete all app_tokens for the user

    Args:
        user: User
        app_token_id: uuid

    Returns: None
    """
    AppToken.objects.delete_app_token(user, app_token_id)


def get_user(app_token_id):
    """
    Get the user for the app_token

    Args:
        app_token_id: uuid
    """
    return AppToken.objects.get_user(app_token_id)


def get_last_token_session_details(user):
    """
    Get the last app token session details for the user

    Args:
        user: User
    """
    apptoken = AppToken.objects.get_last_session(user)
    if apptoken is not None:
        return UserAppTokenSerializer(apptoken).data
    return apptoken


def get_app_token_if_valid(user, app_token_id, serialized=False):
    """
    Get app_token for the user given the app_token_id

    Args:
        user: User
        app_token_id: uuid
    """
    app_token = AppToken.objects.get_app_token_if_valid(user, app_token_id)
    if app_token is not None and serialized:
        return AppTokenSerializer(app_token).data
    return app_token


def get_all_app_tokens(user, serialized=False):
    app_tokens = AppToken.filter(user=user)
    if serialized:
        return AppTokenSerializer(app_tokens, many=True).data
    return app_tokens


def get_all_active_app_tokens(user, serialized=False):
    app_tokens = AppToken.filter(user=user, is_valid=True)
    if serialized:
        return AppTokenSerializer(app_tokens, many=True).data
    return app_tokens


def delete_all_app_tokens(user):
    AppToken.filter(user=user, is_valid=True).delete()
    return None


def delete_all_app_tokens_except(user, app_token_id):
    AppToken.filter(user=user, is_valid=True).exclude(pk=app_token_id).delete()
    return None
