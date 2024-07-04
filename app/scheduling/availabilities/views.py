from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from datetime import datetime
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from organizations.api import get_user_org, get_org_user_from_id
from roles.permissions import HasPermission
from utils.error_handling.error_message import ErrorMessage
from ..base_permissions import VIEW_ALL_AVAILABILITIES, MODIFY_ALL_AVAILABILITIES
from .models import Availability
from .serializers import AvailabilitySerializer


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_ALL_AVAILABILITIES)])
def list_all(request, user_id):
    org = get_user_org(get_request_user(request))
    user = get_org_user_from_id(user_id, org)
    if user:
        availabilities = Availability.objects.filter(user=user)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)
    return ErrorMessage(
        detail='User not found',
        status=404,
        code='UserNotFound',
        instance=request.build_absolute_uri(),
        title='User Not Found'
    ).to_response()


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(MODIFY_ALL_AVAILABILITIES)])
def add_availability(request):
    org = get_user_org(get_request_user(request))
    print(request.data)
    start_time = request.data.get('start_time')  # 2024-07-03T18:00:00.000Z
    start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ').time()
    end_time = request.data.get('end_time')
    end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ').time()
    start_date = request.data.get('start_date')  # 2024-07-03
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = request.data.get('end_date')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    days = request.data.get('days')
    user = get_org_user_from_id(request.data.get('user'), org)
    if user is None:
        return ErrorMessage(
            detail='User not found',
            status=404,
            code='NotFound',
            instance=request.build_absolute_uri(),
            title='Not Found'
        ).to_response()
    user = user.id
    response = []
    if len(days) > 0:
        for day in days:
            serializer = AvailabilitySerializer(data={
                'user': user,
                'start_time': start_time,
                'end_time': end_time,
                'start_date': start_date,
                'end_date': end_date,
                'day': day
            })
            if serializer.is_valid():
                serializer.save()
                response.append(serializer.data)
            else:
                return ErrorMessage(
                    detail=serializer.errors,
                    status=400,
                    code='BadRequest',
                    instance=request.build_absolute_uri(),
                    title='Bad Request'
                ).to_response()
    else:
        if end_date is None:
            end_date = start_date
        serializer = AvailabilitySerializer(data={
            'user': user,
            'start_time': start_time,
            'end_time': end_time,
            'start_date': start_date,
            'end_date': end_date
        })
        if serializer.is_valid():
            serializer.save()
            response.append(serializer.data)
        else:
            return ErrorMessage(
                detail=serializer.errors,
                status=400,
                code='BadRequest',
                instance=request.build_absolute_uri(),
                title='Bad Request'
            ).to_response()
    return Response(response, status=201)


class AvailabilityView(APIView):
    def get(self, request, availability_id):
        pass

    def put(self, request, availability_id):
        pass

    def delete(self, request, availability_id):
        pass
