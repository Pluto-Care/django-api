from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from organizations.api import get_user_org, get_org_user_from_id
from roles.permissions import HasPermission
from ..base_permissions import VIEW_ALL_AVAILABILITIES
from .models import Availability


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_ALL_AVAILABILITIES)])
def list_all(request, user_id):
    org = get_user_org(get_request_user(request))
    user = get_org_user_from_id(user_id, org)
    if user:
        availabilities = Availability.objects.filter(user=user)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_ALL_AVAILABILITIES)])
def add_availability(request):
    pass


class AvailabilityView(APIView):
    def get(self, request, availability_id):
        pass

    def put(self, request, availability_id):
        pass

    def delete(self, request, availability_id):
        pass
