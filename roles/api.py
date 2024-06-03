from .models import Role, Permission, UserRole, UserPermission
from .base import base_permission


def assign_role_to_user(user, role_id):
    if user is None:
        raise ValueError('User is required')
    if role_id is None:
        raise ValueError('Role ID is required')
    role = Role.objects.get(id=role_id)
    user_role = UserRole(user=user, role=role)
    user_role.save()
    return user_role


def assign_permission_to_user(user, permission_id):
    if isinstance(permission_id, dict):
        permission_id = permission_id['id']
    if user is None:
        raise ValueError('User is required')
    if permission_id is None:
        raise ValueError('Permission ID is required')
    permission = Permission.objects.get(id=permission_id)
    user_permission = UserPermission(user=user, permission=permission)
    user_permission.save()
    return user_permission


def check_user_for_permission(user, permission_id):
    if user is None:
        raise ValueError('User is required')
    if permission_id is None:
        raise ValueError('Permission ID is required')
    # Check for explicit permission
    if UserPermission.objects.filter(user=user, permission_id=permission_id).exists():
        return True
    # Check for role permission
    try:
        user_role = UserRole.objects.select_related(
            'role').get(user=user)
        if user_role:
            # Check if user has full access
            if user_role.role.permissions.filter(id=base_permission['FULL_ACCESS']).exists():
                return True
            if user_role.role.permissions.filter(id=permission_id).exists():
                return True
    except UserRole.DoesNotExist:
        pass
    # No permission found
    return False


def has_full_access(user):
    if user is None:
        raise ValueError('User is required')
    return check_user_for_permission(user, base_permission['FULL_ACCESS'])


def get_active_user_permissions(request):
    return getattr(request, 'active_permissions', [])
