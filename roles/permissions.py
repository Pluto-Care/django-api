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

    You may also give list of permissions. If any of the permissions
    is found in user's permissions, access is granted.

    ```
    @permission_classes([HasPermission([READ_USER, READ_ALL_USERS])])
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
        # User role
        user_role = get_active_user_role(request)
        # User explicit permissions
        user_perms = get_active_user_permissions(request)
        # put all permissions into one list
        users_perm_list = []
        if user_role:
            users_perm_list = user_role.get('permissions', [])
        if user_perms:
            ids = [p.get('id') for p in user_perms]
            users_perm_list.extend(ids)
        # Check if user has full access
        if FULL_ACCESS['id'] in users_perm_list:
            return True
        # Check if user has required permission
        if isinstance(self.permission_id, dict):
            self.permission_id = self.permission_id['id']
        if isinstance(self.permission_id, list):
            for perm in self.permission_id:
                if perm in users_perm_list:
                    return True
        elif isinstance(self.permission_id, str):
            if self.permission_id in users_perm_list:
                return True
        raise exceptions.PermissionDenied(self.message)
