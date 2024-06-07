from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.permissions import HasSessionOrTokenActive
from roles.permissions import HasPermission
from .base_permissions import VIEW_PATIENTS, CREATE_PATIENTS, UPDATE_PATIENTS, DELETE_PATIENTS
from .models import Patient
from .serializers import PatientSerializer


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_PATIENTS)])
def listPatients(request):
    patients = Patient.objects.list_patients(request)
    return Response(PatientSerializer(patients, many=True).data, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(CREATE_PATIENTS)])
def createPatient(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        patient = Patient.objects.create_patient(
            request, **serializer.validated_data)
        return Response(PatientSerializer(patient).data, status=201)
    return Response(serializer.errors, status=400)
