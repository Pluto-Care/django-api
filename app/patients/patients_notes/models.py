import uuid
from django.db import models
from django.utils.timezone import now
from users.models import User
from django_cryptography.fields import encrypt
from app.patients.models import Patient


class GeneralNote(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    note = encrypt(models.TextField())
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patient_general_note_created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patient_general_note_updated_by')
    mark_deleted = models.BooleanField(default=False)


class DoctorNote(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    note = encrypt(models.TextField())
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patient_doc_note_created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patient_doc_note_updated_by')
    mark_deleted = models.BooleanField(default=False)
