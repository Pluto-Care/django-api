from django.db import models
from organizations.api import get_user_org
from users.api import get_request_user


class PatientManager(models.Manager):
    """
    This manager works with the Patient model to provide CRUD operations.

    IMPORTANT: Check if the organization of the user making the request
    is the same as the organization of the patient. Otherwise, this is a
    big security risk. Do not make custom queries and use the ones available
    in this model manager.
    """

    def __init__(self):
        super().__init__()

    def create_patient(self, request, **extra_fields):
        patient = self.model(**extra_fields)
        patient.organization = get_user_org(get_request_user(request))
        patient.created_by = get_request_user(request)
        patient.save()
        return patient

    def update_patient(self, request, patient_id, **extra_fields):
        patient = self.model.objects.get(id=patient_id)
        if get_user_org(get_request_user(request)) != patient.organization:
            raise PermissionError(
                'You are not authorized to update this patient')
        for key, value in extra_fields.items():
            if key == 'organization':
                continue
            setattr(patient, key, value)
        patient.updated_by = get_request_user(request)
        patient.save()
        return patient

    def list_patients(self, request):
        return self.model.objects.filter(organization=get_user_org(get_request_user(request)))

    def view_patient(self, request, patient_id):
        patient = self.model.objects.get(id=patient_id)
        if get_user_org(get_request_user(request)) != patient.organization:
            raise PermissionError(
                'You are not authorized to view this patient')
        return patient

    def delete_patient(self, request, patient_id):
        patient = self.model.objects.get(id=patient_id)
        if get_user_org(get_request_user(request)) != patient.organization:
            raise PermissionError(
                'You are not authorized to delete this patient')
        patient.delete()
        return True

    def search_patient(self, request, keyword):
        organization = get_user_org(get_request_user(request))
        patients = self.model.objects.filter(
            models.Q(first_name__startswith=keyword) | models.Q(
                last_name__startswith=keyword),
            organization=organization).values('id', 'first_name', 'last_name', 'phone', 'city', 'state')
        return patients
