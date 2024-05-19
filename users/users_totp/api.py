##########################################################
#
#                   Outward facing API
#
# This file should ideally be the only export from this
# module/app. (Except permissions.py, middlewares.py)
#
# Using imports from other files may breach security.
#
# For API requests, use the urls.py file endpoints.
#
# If you need to use any other function from this package,
# consider making a new function here and calling that.
#
##########################################################

from .models import Totp
from django.db.models import Q


def has_totp(user):
    """
    Check if the user has TOTP enabled

    Args:
        user (User): Model object

    Returns: TOTP or None
    """
    try:
        totp = Totp.objects.get(Q(user=user), ~Q(
            status='disabled'), ~Q(status='initialized'))
        return totp
    except Totp.DoesNotExist:
        return None


def authenticate_totp(user, token, totp_row=None):
    """
    Authenticate the user using the 6 or 8 length token.
    Only send request to this method if `has_totp` returns Totp object,
    otherwise it will produce an Exception.

    Args:
        user (User): Model object
        token (str): 6 or 8 length token

    Returns: bool
    """
    if totp_row is None:
        totp_row = has_totp(user)
        if totp_row is None:
            return False
    return True if Totp.objects.authenticate(user, token, totp_row) else False
