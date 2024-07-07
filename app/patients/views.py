from django.utils.encoding import force_str
from django.db.models import Q
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from roles.permissions import HasPermission
from organizations.api import get_user_org
from users.api import get_request_user
from users.serializers import UserSerializer
from .base_permissions import VIEW_ALL_PATIENTS, CREATE_PATIENTS, UPDATE_PATIENTS, DELETE_PATIENTS
from .models import Patient, PatientNote
from .serializers import PatientSerializer, SearchPatientSerializer, PatientNoteSerializer
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


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive])
def get_patient_notes(request, patient_id):
    organization = get_user_org(get_request_user(request))
    patient_notes = PatientNote.objects.select_related('patient__created_by', 'patient__updated_by').filter(Q(patient__organization=organization) & Q(
        patient__id=patient_id) & Q(mark_deleted=False)).order_by('-created_at')
    response = []
    for note in patient_notes:
        response.append({
            **PatientNoteSerializer(note).data,
            'created_by': UserSerializer(note.created_by).data,
            'updated_by': UserSerializer(note.updated_by).data
        })
    return Response(response, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive])
def create_patient_note(request, patient_id):
    serializer = PatientNoteSerializer(data={
        'note': force_str(request.data['note']),
        'patient': patient_id
    })
    if serializer.is_valid():
        note_text = serializer.validated_data['note']
        # Check if the patient belongs to the organization
        try:
            patient = Patient.objects.get(id=patient_id, organization=get_user_org(
                get_request_user(request)), mark_deleted=False)
        except Patient.DoesNotExist:
            return ErrorMessage(
                title='Patient not found',
                detail='The patient you are looking for does not exist',
                status=404,
                instance=request.build_absolute_uri(),
                code='PatientNotFound'
            ).to_response()
        note = PatientNote.objects.create(
            patient=patient,
            note=note_text,
            created_by=get_request_user(request)
        )
        return Response(PatientNoteSerializer(note).data, status=201)
    return ErrorMessage(
        title='Invalid data',
        status=400,
        instance=request.build_absolute_uri(),
        detail=serializer.errors,
        code='InvalidData'
    ).to_response()


class PatientNoteView(APIView):

    def get(self, request, *args, **kwargs):
        organization = get_user_org(get_request_user(request))
        note_id = force_str(self.kwargs.get('note_id'))
        note = PatientNote.objects.get(
            id=note_id, patient__organization=organization)
        if note.mark_deleted:
            return ErrorMessage(
                title='Note not found',
                detail='The note you are looking for does not exist',
                status=404,
                instance=request.build_absolute_uri(),
                code='NoteNotFound'
            ).to_response()
        return Response(PatientNoteSerializer(note).data, status=200)

    def put(self, request, *args, **kwargs):
        note_id = force_str(self.kwargs.get('note_id'))
        serializer = PatientNoteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                note = PatientNote.objects.get(
                    id=note_id, patient__organization=get_user_org(get_request_user(request)), mark_deleted=False)
            except PatientNote.DoesNotExist:
                return ErrorMessage(
                    title='Note not found',
                    detail='The note you are looking for does not exist',
                    status=404,
                    instance=request.build_absolute_uri(),
                    code='NoteNotFound'
                ).to_response()
            # Check if the user is the creator of the note
            if note.created_by != get_request_user(request):
                return ErrorMessage(
                    title='Unauthorized',
                    status=403,
                    instance=request.build_absolute_uri(),
                    detail='You are not authorized to update this note',
                    code='UnauthorizedNoteUpdate'
                )
            note.note = serializer.validated_data['note']
            note.updated_by = get_request_user(request)
            note.updated_at = now()
            note.save()
            return Response(PatientNoteSerializer(note).data, status=200)
        return ErrorMessage(
            title='Invalid data',
            status=400,
            instance=request.build_absolute_uri(),
            detail=serializer.errors,
            code='InvalidData'
        ).to_response()

    def delete(self, request, *args, **kwargs):
        note_id = force_str(self.kwargs.get('note_id'))
        try:
            note = PatientNote.objects.get(
                id=note_id, patient__organization=get_user_org(get_request_user(request)))
        except PatientNote.DoesNotExist:
            return ErrorMessage(
                title='Note not found',
                detail='The note you are looking for does not exist',
                status=404,
                instance=request.build_absolute_uri(),
                code='NoteNotFound'
            ).to_response()
        # Check if the user is the creator of the note
        if note.created_by != get_request_user(request):
            return ErrorMessage(
                title='Unauthorized',
                status=403,
                instance=request.build_absolute_uri(),
                detail='You are not authorized to delete this note',
                code='UnauthorizedNoteDelete'
            )
        note.mark_deleted = True
        note.save()
        return Response(data={}, status=200)
