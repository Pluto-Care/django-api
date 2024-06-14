from django.db import models


class AppointmentManager(models.Manager):
    def __init__(self):
        super().__init__()

    def get_appointment(self, organization, appointment_id, assinged_to=None):
        """Get an appointment by its ID

        Args:
            organization (Organization): The organization the appointment belongs to
            appointment_id (string): The ID of the appointment

        Raises:
            ValueError: If the appointment does not exist

        Returns:
            Appointment: The appointment object
        """
        try:
            if assinged_to:
                appointment = self.model.objects.get(
                    id=appointment_id, organization=organization, assigned_to=assinged_to)
            else:
                appointment = self.model.objects.get(
                    id=appointment_id, organization=organization)
        except self.model.DoesNotExist:
            raise ValueError(
                'The appointment you are looking for does not exist')
        return appointment

    def make_appointment(self, **extra_fields):
        """
        Make new appointment

        Args:
            raw field data

        Returns:
            Appointment: The appointment object
        """
        appointment = self.create(
            **extra_fields
        )
        return appointment

    def cancel_appointment(self, organization, appointment_id):
        """Cancel appointment

        Args:
            organization (Organization): The organization the appointment belongs to
            appointment_id (string): The ID of the appointment

        Returns:
            Appointment: The appointment object
        """
        appointment = self.get_appointment(organization, appointment_id)
        appointment.status = 'cancelled'
        appointment.save()
        return appointment
