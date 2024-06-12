from models import Patient


def get_patient(request, patient_id):
    return Patient.objects.view_patient(request, patient_id)
