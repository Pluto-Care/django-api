from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from django.db.models import Q
from django.utils.timezone import now
from organizations.api import get_user_org
from users.api import get_request_user
from users.serializers import UserSerializer
from utils.error_handling.error_message import ErrorMessage
from roles.permissions import HasPermission
from app.patients.models import Patient
from .models import GeneralNote, DoctorNote
from .serializers import GeneralNoteSerializer, DoctorNoteSerializer
from .base_permissions import CREATE_DOCTOR_NOTES, VIEW_DOCTOR_NOTES


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive])
def get_general_notes(request, patient_id):
    organization = get_user_org(get_request_user(request))
    patient_notes = GeneralNote.objects.select_related('patient__created_by', 'patient__updated_by').filter(Q(patient__organization=organization) & Q(
        patient__id=patient_id) & Q(mark_deleted=False)).order_by('-created_at')
    response = []
    for note in patient_notes:
        response.append({
            **GeneralNoteSerializer(note).data,
            'created_by': UserSerializer(note.created_by).data,
            'updated_by': UserSerializer(note.updated_by).data
        })
    return Response(response, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive])
def create_general_note(request, patient_id):
    serializer = GeneralNoteSerializer(data={
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
        note = GeneralNote.objects.create(
            patient=patient,
            note=note_text,
            created_by=get_request_user(request)
        )
        return Response(GeneralNoteSerializer(note).data, status=201)
    return ErrorMessage(
        title='Invalid data',
        status=400,
        instance=request.build_absolute_uri(),
        detail=serializer.errors,
        code='InvalidData'
    ).to_response()


class GeneralNoteView(APIView):

    def get(self, request, *args, **kwargs):
        organization = get_user_org(get_request_user(request))
        note_id = force_str(self.kwargs.get('note_id'))
        note = GeneralNote.objects.get(
            id=note_id, patient__organization=organization)
        if note.mark_deleted:
            return ErrorMessage(
                title='Note not found',
                detail='The note you are looking for does not exist',
                status=404,
                instance=request.build_absolute_uri(),
                code='NoteNotFound'
            ).to_response()
        return Response(GeneralNoteSerializer(note).data, status=200)

    def put(self, request, *args, **kwargs):
        note_id = force_str(self.kwargs.get('note_id'))
        serializer = GeneralNoteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                note = GeneralNote.objects.get(
                    id=note_id, patient__organization=get_user_org(get_request_user(request)), mark_deleted=False)
            except GeneralNote.DoesNotExist:
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
            return Response(GeneralNoteSerializer(note).data, status=200)
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
            note = GeneralNote.objects.get(
                id=note_id, patient__organization=get_user_org(get_request_user(request)))
        except GeneralNote.DoesNotExist:
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


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(VIEW_DOCTOR_NOTES)])
def get_doctor_notes(request, patient_id):
    organization = get_user_org(get_request_user(request))
    doctor_notes = DoctorNote.objects.select_related('patient__created_by', 'patient__updated_by').filter(Q(patient__organization=organization) & Q(
        patient__id=patient_id) & Q(mark_deleted=False)).order_by('-created_at')
    response = []
    for note in doctor_notes:
        response.append({
            **DoctorNoteSerializer(note).data,
            'created_by': UserSerializer(note.created_by).data,
            'updated_by': UserSerializer(note.updated_by).data
        })
    return Response(response, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(CREATE_DOCTOR_NOTES)])
def create_doctor_note(request, patient_id):
    serializer = DoctorNoteSerializer(data={
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
        note = DoctorNote.objects.create(
            patient=patient,
            note=note_text,
            created_by=get_request_user(request)
        )
        return Response(DoctorNoteSerializer(note).data, status=201)
    return ErrorMessage(
        title='Invalid data',
        status=400,
        instance=request.build_absolute_uri(),
        detail=serializer.errors,
        code='InvalidData'
    ).to_response()


class DoctorNoteView(APIView):

    def get(self, request, *args, **kwargs):
        organization = get_user_org(get_request_user(request))
        note_id = force_str(self.kwargs.get('note_id'))
        note = DoctorNote.objects.get(
            id=note_id, patient__organization=organization)
        if note.mark_deleted:
            return ErrorMessage(
                title='Note not found',
                detail='The note you are looking for does not exist',
                status=404,
                instance=request.build_absolute_uri(),
                code='NoteNotFound'
            ).to_response()
        return Response(DoctorNoteSerializer(note).data, status=200)

    def put(self, request, *args, **kwargs):
        note_id = force_str(self.kwargs.get('note_id'))
        serializer = DoctorNoteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                note = DoctorNote.objects.get(
                    id=note_id, patient__organization=get_user_org(get_request_user(request)), mark_deleted=False)
            except DoctorNote.DoesNotExist:
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
            return Response(DoctorNoteSerializer(note).data, status=200)
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
            note = DoctorNote.objects.get(
                id=note_id, patient__organization=get_user_org(get_request_user(request)))
        except DoctorNote.DoesNotExist:
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
