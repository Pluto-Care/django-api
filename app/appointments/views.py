import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from organizations.api import get_user_org
from roles.permissions import HasPermission
from .base_permissions import MODIFY_APPOINTMENTS, VIEW_APPOINTMENTS, MAKE_APPOINTMENTS
from .models import Appointment
from .serializers import AppointmentSerializer
from utils.error_handling.error_message import ErrorMessage


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(MAKE_APPOINTMENTS)])
def create_appointment(request):
    organization = get_user_org(get_request_user(request))
    created_by = get_request_user(request)
    # Format: 'date': '2024-06-13T07:00:00.000Z', 'start_time': '10:30', 'duration': 30,
    start_at = datetime.datetime.strptime(
        request.data['date'], '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=int(request.data['start_time'].split(':')[0]), minutes=int(request.data['start_time'].split(':')[1]))
    end_at = start_at + datetime.timedelta(minutes=request.data['duration'])
    # Create appointment
    serializer = AppointmentSerializer(data=dict(
        patient=request.data['patient'],
        reason=request.data['reason'],
        assigned_to=request.data['assigned_to'],
        status=request.data['status'],
        start_at=start_at,
        end_at=end_at,
        organization=organization.id,
        created_by=created_by.id,
    ))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_APPOINTMENTS)])
def list_appointments(request):
    organization = get_user_org(get_request_user(request))
    appointments = Appointment.objects.select_related('patient', 'assigned_to', 'created_by').filter(
        organization=organization).order_by('created_at')
    result = []
    for appointment in appointments:
        serialized = AppointmentSerializer(appointment).data
        assigned_to = dict(
            id=appointment.assigned_to.id,
            first_name=appointment.assigned_to.first_name,
            last_name=appointment.assigned_to.last_name,
        )
        patient = dict(
            id=appointment.patient.id,
            first_name=appointment.patient.first_name,
            last_name=appointment.patient.last_name,
            phone=appointment.patient.phone,
            email=appointment.patient.email,
        )
        if appointment.created_by:
            created_by = dict(
                id=appointment.created_by.id,
                first_name=appointment.created_by.first_name,
                last_name=appointment.created_by.last_name,
            )
        else:
            created_by = None
        if appointment.updated_by:
            updated_by = dict(
                id=appointment.updated_by.id,
                first_name=appointment.updated_by.first_name,
                last_name=appointment.updated_by.last_name,
            )
        else:
            updated_by = None
        result.append({
            **serialized,
            'assigned_to': assigned_to,
            'patient': patient,
            'created_by': created_by,
            'updated_by': updated_by
        })
    return Response(result, status=200)


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
        organization=organization, assigned_to=get_request_user(request)).order_by('created_at')
    result = []
    for appointment in appointments:
        serialized = AppointmentSerializer(appointment).data
        assigned_to = dict(
            id=appointment.assigned_to.id,
            first_name=appointment.assigned_to.first_name,
            last_name=appointment.assigned_to.last_name,
        )
        patient = dict(
            id=appointment.patient.id,
            first_name=appointment.patient.first_name,
            last_name=appointment.patient.last_name,
            phone=appointment.patient.phone,
            email=appointment.patient.email,
        )
        if appointment.created_by:
            created_by = dict(
                id=appointment.created_by.id,
                first_name=appointment.created_by.first_name,
                last_name=appointment.created_by.last_name,
            )
        else:
            created_by = None
        if appointment.updated_by:
            updated_by = dict(
                id=appointment.updated_by.id,
                first_name=appointment.updated_by.first_name,
                last_name=appointment.updated_by.last_name,
            )
        else:
            updated_by = None
        result.append({
            **serialized,
            'assigned_to': assigned_to,
            'patient': patient,
            'created_by': created_by,
            'updated_by': updated_by
        })
    return Response(result, status=200)
