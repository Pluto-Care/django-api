from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from roles.permissions import HasPermission
from .base_permissions import VIEW_ALL_PATIENTS, CREATE_PATIENTS, UPDATE_PATIENTS, DELETE_PATIENTS
from .models import Patient
from .serializers import PatientSerializer, SearchPatientSerializer
from utils.error_handling.error_message import ErrorMessage


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_ALL_PATIENTS)])
def listPatients(request):
    patients = Patient.objects.list_patients(request)
    return Response(PatientSerializer(patients, many=True).data, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive])
def search_patient(request):
    keyword = force_str(request.data['keyword'])
    patients = Patient.objects.search_patient(request, keyword)
    return Response(SearchPatientSerializer(patients, many=True).data, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(CREATE_PATIENTS)])
def createPatient(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        patient = Patient.objects.create_patient(
            request, **serializer.validated_data)
        return Response(PatientSerializer(patient).data, status=201)
    return ErrorMessage(
        title='Invalid data',
        status=400,
        instance=request.build_absolute_uri(),
        detail=serializer.errors,
        code='InvalidData'
    ).to_response()


class PatientView(APIView):

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [HasSessionOrTokenActive(), HasPermission(UPDATE_PATIENTS)]
        elif self.request.method == 'DELETE':
            return [HasSessionOrTokenActive(), HasPermission(DELETE_PATIENTS)]
        elif self.request.method == 'GET':
            return [HasSessionOrTokenActive()]
        return [HasPermission("patient_view_reject")]

    def get(self, request, *args, **kwargs):
        patient_id = force_str(self.kwargs.get('patient_id'))
        patient = Patient.objects.view_patient(request, patient_id)
        return Response(PatientSerializer(patient).data, status=200)

    def put(self, request, *args, **kwargs):
        patient_id = force_str(self.kwargs.get('patient_id'))
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = Patient.objects.update_patient(
                request, patient_id, **serializer.validated_data)
            return Response(PatientSerializer(patient).data, status=200)
        return ErrorMessage(
            title='Invalid data',
            status=400,
            instance=request.build_absolute_uri(),
            detail=serializer.errors,
            code='InvalidData'
        ).to_response()

    def delete(self, request, *args, **kwargs):
        patient_id = force_str(self.kwargs.get('patient_id'))
        Patient.objects.delete_patient(request, patient_id)
        return Response(status=204)
