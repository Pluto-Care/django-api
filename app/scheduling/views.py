from rest_framework.decorators import api_view, permission_classes
from app.scheduling.base_permissions import MODIFY_ALL_APPOINTMENTS
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from organizations.api import get_user_org, get_org_user_from_id
from roles.permissions import HasPermission


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(MODIFY_ALL_APPOINTMENTS)])
def getAvailableTimeSlots(request, timezone, user_id):
    org = get_user_org(get_request_user(request))
    user = get_org_user_from_id(user_id, org)
