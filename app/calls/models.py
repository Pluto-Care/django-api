import uuid
from django.db import models
from django.utils.timezone import now
from users.models import User
from app.patients.models import Patient


class OutgoingCallLog(models.Model):
    status_choices = [
        ('completed', 'completed'),
        ('failed', 'failed'),
        ('busy', 'busy'),
        ('no-answer', 'no-answer'),
        ('canceled', 'canceled'),
        ('initiated', 'initiated'),
    ]

    twilio_call_id = models.CharField(
        primary_key=True, max_length=34, editable=False)
    to = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    duration = models.IntegerField()
    status = models.CharField(max_length=10, choices=status_choices)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.call_id
