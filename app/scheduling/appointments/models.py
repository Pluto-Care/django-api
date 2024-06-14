import uuid
from django.utils.timezone import now
from django.db import models
from app.patients.models import Patient
from organizations.models import Organization
from users.models import User
from .managers import AppointmentManager


class Appointment(models.Model):
    status = (
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled')
    )
    type = (
        ('in-person', 'In-Person'),
        ('video', 'Video'),
        ('phone', 'Phone')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(
        max_length=16, choices=status, default='confirmed')
    type = models.CharField(max_length=16, choices=type, default='phone')
    start_time = models.DateTimeField()
    end_time_expected = models.DateTimeField(default=None, null=True)
    end_time = models.DateTimeField(null=True, default=None)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='appointment_created_by')
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='appointment_assigned_to', default=None)
    updated_at = models.DateTimeField(default=now)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='appointment_updated_by')
    logs = models.JSONField(default=dict)

    objects = AppointmentManager()

    class Meta:
        indexes = [
            models.Index(fields=['start_time', 'status', 'type']),
        ]
        # constraint that end_time and end_time_expected should be greater than start_time
        # constraint that start_time should be greater than current time
        constraints = [
            models.CheckConstraint(check=models.Q(
                end_time__gt=models.F('start_time')), name='apt_end_time_gt_start_time'),
            models.CheckConstraint(check=models.Q(
                end_time_expected__gt=models.F('start_time')), name='apt_end_time_expected_gt_start_time'),
            models.CheckConstraint(check=models.Q(
                start_time__gt=now()), name='apt_start_time_gt_now')
        ]

    def __str__(self):
        return f"{self.pk}"


class Cancellation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    reason = models.TextField()
    cancelled_at = models.DateTimeField(default=now)
    cancelled_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='cancellation_created_by')

    def __str__(self):
        return f"{self.pk}"
