from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from utils.error_handling.error_message import ErrorMessage
from organizations.api import get_org_user, get_user_org
from users.api import get_request_user
from users.permissions import HasSessionOrTokenActive
from .permissions import HasPermission
from .base_permissions import MODIFY_USER_PERMISSIONS
from .models import UserPermission


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(MODIFY_USER_PERMISSIONS)])
def update_permissions(request):
    """Update user permissions. Takes a list of permissions and mirror it to the user.

    Post data example:
    ```json
    {
        "user_id": 1,
        "permissions": ["update:organization", "read:all_logs"]
    }
    ```
    """
    requested_permissions = request.data['permissions']
    if isinstance(requested_permissions, list):
        user_id = request.data['user_id']
        organization = get_user_org(get_request_user(request))
        actioned_user = get_org_user(user_id, organization)
        if actioned_user is None:
            return ErrorMessage(
                title='User Not Found',
                detail='User not found.',
                instance=request.build_absolute_uri(),
                status=404,
                code='UserNotFound',
            ).to_response()
        actioned_user_permissions = UserPermission.objects.select_related(
            'permission').filter(user=actioned_user)
        # If user had permission but new permission list does not contain it, remove it
        # vice versa, if user did not have permission but new permission list contains it, add it
        for actioned_user_permission in actioned_user_permissions:
            # If permission is not in new permission list, remove it
            if actioned_user_permission.permission.id not in requested_permissions:
                actioned_user_permission.delete()
        actioned_user_permissions_ids = [
            actioned_user_permission.permission.id for actioned_user_permission in actioned_user_permissions]
        for permission_id in requested_permissions:
            # If permission is not in user permissions, add it
            if permission_id not in actioned_user_permissions_ids:
                user_permission = UserPermission(
                    user=actioned_user, permission_id=permission_id)
                user_permission.save()
        return Response(status=200, data={'message': 'Permissions updated successfully'})
    return ErrorMessage(
        title='Invalid Permissions',
        detail='Permissions must be a list.',
        instance=request.build_absolute_uri(),
        status=400,
        code='InvalidPermissions',
    ).to_response()
