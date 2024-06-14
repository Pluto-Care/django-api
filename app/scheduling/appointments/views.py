import datetime
from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from organizations.api import get_user_org
from roles.permissions import HasPermission
from .base_permissions import MODIFY_APPOINTMENTS, VIEW_APPOINTMENTS, MAKE_APPOINTMENTS
from .models import Appointment, Cancellation
from .serializers import AppointmentSerializer
from utils.error_handling.error_message import ErrorMessage


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(MAKE_APPOINTMENTS)])
def create_appointment(request):
    organization = get_user_org(get_request_user(request))
    created_by = get_request_user(request)
    # Format: 'date': '2024-06-13T07:00:00.000Z', 'start_time': '10:30', 'duration': 30,
    start_at = datetime.datetime.strptime(
        force_str(request.data['date']),
        '%Y-%m-%dT%H:%M:%S.%fZ'
    ) + datetime.timedelta(
        hours=int(force_str(request.data['start_time']).split(':')[0]),
        minutes=int(force_str(request.data['start_time']).split(':')[1])
    )
    end_at = start_at + \
        datetime.timedelta(minutes=int(force_str(request.data['duration'])))
    # Create appointment
    serializer = AppointmentSerializer(data=dict(
        patient=force_str(request.data['patient']),
        reason=force_str(request.data['reason']),
        assigned_to=force_str(request.data['assigned_to']),
        status=force_str(request.data['status']),
        type=force_str(request.data['type']),
        start_time=start_at,
        end_time_expected=end_at,
        end_time=None,
        organization=organization.id,
        created_by=created_by.id,
    ))
    if serializer.is_valid():
        serializer.save()
        appointment_obj = serializer.instance
        return Response(format_appointments([appointment_obj])[0], status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_APPOINTMENTS)])
def list_appointments(request):
    organization = get_user_org(get_request_user(request))
    appointments = Appointment.objects.select_related('patient', 'assigned_to', 'created_by', 'updated_by').filter(
        organization=organization).order_by('-created_at')
    return Response(format_appointments(appointments), status=200)


class AdminAppointmentView(APIView):

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [HasSessionOrTokenActive(), HasPermission(MODIFY_APPOINTMENTS)]
        elif self.request.method == 'DELETE':
            return [HasSessionOrTokenActive(), HasPermission(MODIFY_APPOINTMENTS)]
        elif self.request.method == 'GET':
            return [HasSessionOrTokenActive(), HasPermission(VIEW_APPOINTMENTS)]
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
            Cancellation.objects.create(
                appointment=appointment,
                reason='Appointment cancelled by admin',
                cancelled_by=get_request_user(request)
            )
        except (ValueError, PermissionError) as error:
            return ErrorMessage(
                title='Appointment not found',
                detail=error,
                status=404,
                instance=request.build_absolute_uri(),
                code='AppointmentNotFound'
            ).to_response()
        return Response(appointment, status=200)


class MyAppointmentView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [HasSessionOrTokenActive()]
        return [False]

    def get(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get('appointment_id')
        try:
            appointment = Appointment.objects.get_appointment(
                appointment_id, assinged_to=get_request_user(request))
            return Response(AppointmentSerializer(appointment).data, status=200)
        except Appointment.DoesNotExist:
            return ErrorMessage(
                title='Appointment not found',
                detail='The appointment you are looking for does not exist',
                status=404,
                instance=request.build_absolute_uri(),
                code='AppointmentNotFound'
            ).to_response()


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive])
def my_appointments(request):
    organization = get_user_org(get_request_user(request))
    appointments = Appointment.objects.select_related('patient', 'assigned_to', 'created_by').filter(
        organization=organization, assigned_to=get_request_user(request)).order_by('-created_at')
    return Response(format_appointments(appointments), status=200)


# Fomat the appointment data
def format_appointments(appointments):
    result = []
    for appointment in appointments:
        # Get appointment data
        serialized = AppointmentSerializer(appointment).data
        # Get patient data
        patient = dict(
            id=appointment.patient.id,
            first_name=appointment.patient.first_name,
            last_name=appointment.patient.last_name,
            phone=appointment.patient.phone,
            email=appointment.patient.email,
        )
        assigned_to, created_by, updated_by = None, None, None
        # Get assigned_to, created_by, updated_by data
        if appointment.assigned_to:
            assigned_to = dict(
                id=appointment.assigned_to.id,
                first_name=appointment.assigned_to.first_name,
                last_name=appointment.assigned_to.last_name,
            )
        if appointment.created_by:
            created_by = dict(
                id=appointment.created_by.id,
                first_name=appointment.created_by.first_name,
                last_name=appointment.created_by.last_name,
            )
        if appointment.updated_by:
            updated_by = dict(
                id=appointment.updated_by.id,
                first_name=appointment.updated_by.first_name,
                last_name=appointment.updated_by.last_name,
            )
        # Append the data to the result
        result.append({
            **serialized,
            'assigned_to': assigned_to,
            'patient': patient,
            'created_by': created_by,
            'updated_by': updated_by
        })
    return result
