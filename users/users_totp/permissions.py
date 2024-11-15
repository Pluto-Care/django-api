from rest_framework import permissions
from django.utils.encoding import force_str
from .models import MFAJoinToken
from rest_framework.permissions import exceptions


class HasMFAJoinToken(permissions.BasePermission):
    message = 'Unauthorized! MFA Join Token is required.'
    """
    Permission to check if user session is present
    """

    def has_permission(self, request, view):
        # Check if request has mfa_join_token
        if 'mfa_join_token' in request.data:
            # Get the MFAJoinToken object
            mfa_join_token = MFAJoinToken.objects.verify_token(
                force_str(request.data['mfa_join_token']), request)
            if mfa_join_token:
                return True
        raise exceptions.ParseError(self.message)
