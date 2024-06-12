from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from organizations.api import get_user_org
from roles.permissions import HasPermission
from .base_permissions import MODIFY_APPOINTMENTS, VIEW_APPOINTMENTS
from .models import Appointment
from .serializers import AppointmentSerializer
from utils.error_handling.error_message import ErrorMessage


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(MODIFY_APPOINTMENTS)])
def create_appointment(request):
    try:
        appointment = Appointment.objects.make_appointment(
            request, **request.data)
    except ValueError as error:
        return ErrorMessage(
            title='Appointment not created',
            detail=error,
            status=400,
            instance=request.build_absolute_uri(),
            code='AppointmentNotCreated'
        ).to_response()
    return Response(AppointmentSerializer(appointment).data, status=201)


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_APPOINTMENTS)])
def list_appointments(request):
    organization = get_user_org(get_request_user(request))
    appointments = Appointment.objects.filter(
        organization=organization).order_by('created_at')
    return Response(AppointmentSerializer(appointments, many=True).data, status=200)


class AppointmentView(APIView):

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [HasSessionOrTokenActive(), HasPermission(MODIFY_APPOINTMENTS)]
        elif self.request.method == 'DELETE':
            return [HasSessionOrTokenActive(), HasPermission(MODIFY_APPOINTMENTS)]
        elif self.request.method == 'GET':
            return [HasSessionOrTokenActive(), HasPermission([VIEW_APPOINTMENTS, MODIFY_APPOINTMENTS])]
        return [False]

    def get(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get('appointment_id')
        try:
            appointments = Appointment.objects.get_appointment(appointment_id)
            return Response(AppointmentSerializer(appointments).data, status=200)
        except Appointment.DoesNotExist:
            return ErrorMessage(
                title='Appointment not found',
                detail='The appointment you are looking for does not exist',
                status=404,
                instance=request.build_absolute_uri(),
                code='AppointmentNotFound'
            ).to_response()

    def delete(self, request, *args, **kwargs):
        # Set the appointment to cancel status
        appointment_id = self.kwargs.get('appointment_id')
        try:
            appointment = Appointment.objects.cancel_appointment(
                request, appointment_id)
        except (ValueError, PermissionError) as error:
            return ErrorMessage(
                title='Appointment not found',
                detail=error,
                status=404,
                instance=request.build_absolute_uri(),
                code='AppointmentNotFound'
            ).to_response()
        return Response(appointment, status=200)
