from django.db.models import Q
from .models import Role, Permission, UserRole, UserPermission
from .base_permissions import base_permission
from .serializers import RoleSerializer, PermissionSerializer


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


def get_user_role(user):
    if user is None:
        raise ValueError('User is required')
    try:
        user_role = UserRole.objects.select_related(
            'role').get(user=user)
        role_serializer = RoleSerializer(user_role.role)
        return role_serializer.data
    except UserRole.DoesNotExist:
        return None


def get_user_permissions(user):
    if user is None:
        raise ValueError('User is required')
    permissions = []
    # Check for explicit permissions
    user_permissions = UserPermission.objects.select_related('permission').filter(
        user=user)
    for user_permission in user_permissions:
        permissions.append(PermissionSerializer(
            user_permission.permission).data)
    return permissions


def check_user_for_permission(user, permission_id):
    if user is None:
        raise ValueError('User is required')
    if permission_id is None:
        raise ValueError('Permission ID is required')
    if isinstance(permission_id, dict):
        permission_id = permission_id['id']
    # Check if user has full access or has explicit permission
    if UserPermission.objects.filter(Q(user=user), Q(permission_id=base_permission['FULL_ACCESS']['id']) | Q(permission_id=permission_id)).exists():
        return True
    # Check for role permission
    try:
        user_role = UserRole.objects.select_related(
            'role').get(user=user)
        if user_role:
            # Check if role has full access or has explicit permission
            if user_role.role.permissions.filter(Q(id=base_permission['FULL_ACCESS']['id']) | Q(id=permission_id)).exists():
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
    return getattr(request, 'active_user_permissions', None)


def get_active_user_role(request):
    return getattr(request, 'active_user_role', None)
