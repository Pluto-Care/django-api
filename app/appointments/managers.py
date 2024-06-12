from django.db import models
from organizations.api import get_user_org, get_org_user
from users.api import get_request_user
from .serializers import AppointmentSerializer


class AppointmentManager(models.Manager):
    def __init__(self):
        super().__init__()

    def get_appointment(self, request, appointment_id):
        appointment = self.model.objects.get(id=appointment_id)
        if get_user_org(get_request_user(request)) != appointment.organization:
            raise PermissionError(
                'You are not authorized to view this appointment')
        return appointment

    def make_appointment(self, request, **extra_fields):
        """
        Return serialized appointment data

        Args:
            request (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        organization = get_user_org(get_request_user(request))
        serializer = AppointmentSerializer(data={
            **extra_fields,
            'organization': organization,
            'created_by': get_org_user(get_request_user(request), organization),
        })
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValueError(serializer.errors)

    def cancel_appointment(self, request, appointment_id):
        try:
            appointment = self.model.objects.get(id=appointment_id)
        except self.model.DoesNotExist:
            raise ValueError(
                'The appointment you are looking for does not exist')
        if get_user_org(get_request_user(request)) != appointment.organization:
            raise PermissionError(
                'You are not authorized to cancel this appointment')
        appointment.status = 'cancelled'
        appointment.save()
        return AppointmentSerializer(appointment).data
