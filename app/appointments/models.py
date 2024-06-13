import uuid
from django.utils.timezone import now
from django.db import models
from app.patients.models import Patient
from organizations.models import Organization
from users.models import User
from .managers import AppointmentManager


class Appointment(models.Model):
    status = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reason = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=status, default='pending')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='appointment_created_by')
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='appointment_assigned_to')
    updated_at = models.DateTimeField(default=now)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='appointment_updated_by')

    objects = AppointmentManager()

    class Meta:
        indexes = [
            models.Index(fields=['start_at']),
        ]

    def __str__(self):
        return f"{self.pk}"
