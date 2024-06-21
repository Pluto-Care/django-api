import uuid
from django.db import models
from django.utils.timezone import now
from users.models import User
from organizations.models import Organization
from django_cryptography.fields import encrypt
from .managers import PatientManager


class Patient(models.Model):
    sex_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = encrypt(models.DateField(blank=True, null=True))
    sex = encrypt(models.CharField(
        max_length=10, choices=sex_choices, blank=True, null=True))
    street = encrypt(models.CharField(max_length=255, blank=True, null=True))
    city = encrypt(models.CharField(max_length=255, blank=True, null=True))
    state = encrypt(models.CharField(max_length=255, blank=True, null=True))
    postal_code = encrypt(models.CharField(
        max_length=10, blank=True, null=True))
    country = encrypt(models.CharField(max_length=255, blank=True, null=True))
    phone = encrypt(models.CharField(max_length=15, blank=True, null=True))
    email = encrypt(models.EmailField(blank=True, null=True))
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patient_created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patient_updated_by')
    mark_deleted = models.BooleanField(default=False)

    objects = PatientManager()

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class PatientNote(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    note = encrypt(models.TextField())
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patient_note_created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patient_note_updated_by')
    mark_deleted = models.BooleanField(default=False)
