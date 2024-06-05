from rest_framework import permissions
from .api import get_active_user_permissions, get_active_user_role
from .base_permissions import FULL_ACCESS
from rest_framework.permissions import exceptions


class HasPermission(permissions.BasePermission):
    """
    Allows access only to users who have the appropriate permission.

    Usage:
    ```
    from .base_permissions import READ_USER

    @permission_classes([HasPermission(READ_USER),])
    def my_view(request):
    ```
    """

    permission_id = ""
    message = "You do not have permission to perform this action."

    def __init__(self, permission_id):
        super().__init__()
        self.permission_id = permission_id

    def __call__(self):
        return self

    def has_permission(self, request, view):
        if isinstance(self.permission_id, dict):
            self.permission_id = self.permission_id['id']
        # User role
        user_role = get_active_user_role(request)
        # User explicit permissions
        user_permissions = get_active_user_permissions(request)
        # put all permissions into one list
        full_permissions = []
        if user_role:
            full_permissions = user_role.get('permissions', [])
        if user_permissions:
            ids = [p.get('id') for p in user_permissions]
            full_permissions.extend(ids)
        print(full_permissions)
        # Check if user has full access
        if FULL_ACCESS['id'] in full_permissions:
            return True
        # Check if user has required permission
        if self.permission_id in full_permissions:
            return True
        raise exceptions.PermissionDenied(self.message)
