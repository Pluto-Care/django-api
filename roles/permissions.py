from rest_framework import permissions
from users.api import get_request_user
from .api import check_user_for_permission
from .base import base_permission

# For base_permission and base_role, see roles/base.py


class HasPermission(permissions.BasePermission):
    """
    Allows access only to users who have the appropriate permission.

    `@permission_classes([HasPermission(base_permission['READ_USER']),])`
    """

    permission_id = ""

    def __init__(self, permission_id):
        super().__init__()
        self.permission_id = permission_id

    def __call__(self):
        return self

    def has_permission(self, request, view):
        user = get_request_user(request)
        return check_user_for_permission(user, self.permission_id)


class HasFullAccess(permissions.BasePermission):
    """
    Allows access only to users who have the appropriate permission.

    `@permission_classes([HasFullAccess,])`
    """

    def has_permission(self, request, view):
        user = get_request_user(request)
        return check_user_for_permission(user, base_permission['FULL_ACCESS']['id'])
