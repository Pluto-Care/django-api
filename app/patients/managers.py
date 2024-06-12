from django.db import models
from organizations.api import get_user_org
from users.api import get_request_user


class PatientManager(models.Manager):
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
