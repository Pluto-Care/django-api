from rest_framework import permissions
from .api import get_active_user_permissions
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
        # Check if user has full access or has explicit permission
        if FULL_ACCESS['id'] in get_active_user_permissions(request):
            return True
        if self.permission_id in get_active_user_permissions(request):
            return True
        raise exceptions.PermissionDenied(self.message)
