from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from utils.error_handling.error_message import ErrorMessage
from decouple import config
# Twilio
from twilio.twiml.voice_response import VoiceResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from .decorators import validate_twilio_request
# User Imports
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from roles.permissions import HasPermission
from .base_permissions import MAKE_CALL
from .models import OutgoingCallLog


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(MAKE_CALL)])
def grant_twilio_token(request):
    """
    Generate a Twilio token for the user to make a call.
    """
    account_sid = config('TWILIO_ACCOUNT_SID')
    api_key = config('TWILIO_API_KEY')
    api_secret = config('TWILIO_API_KEY_SECRET')

    token = AccessToken(
        account_sid=account_sid,
        signing_key_sid=api_key,
        secret=api_secret,
        identity=get_request_user(request).email,
        ttl=3600
    )

    # add grants to token
    token.add_grant(VoiceGrant(
        incoming_allow=False,
        push_credential_sid=config('TWILIO_PUSH_CREDENTIAL_SID'),
        outgoing_application_sid=config('TWILIO_OUTGOING_APPLICATION_SID')
    ))

    return JsonResponse({"token": token.to_jwt()}, status=200, safe=False)


@api_view(['POST'])
@validate_twilio_request
def twiml(request):
    """
    This endpoint is called by Twilio to get the TwiML for the call.
    Twilio authenticates by checking the token that is produced by
    the grant_twilio_token endpoint. This check happens on Twilio
    servers.

    This does not make a call happen, this just returns the TwiML
    that Twilio will use to make the call.
    """
    data = dict(request.data)

    if 'To' not in data:
        return ErrorMessage(
            title='Invalid data provided',
            detail='to is required',
            status=400,
            instance=request.build_absolute_uri()
        ).to_response()

    vr = VoiceResponse()
    vr.dial(
        caller_id=config('TWILIO_PHONE_NUMBER'),
        answer_on_bridge=True
    ).number(data['To'][0])
    # Create an outgoing call log
    OutgoingCallLog.objects.create(
        to=data['To'],
        twilio_call_id=data['CallSid'],
        user=get_request_user(request),
        patient_id=data['patient_id'],
        duration=0,
        status='initiated'
    )
    # Return the TwiML
    return HttpResponse(vr.to_xml(), content_type='text/xml')


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive])
def register_call_status(request):
    data = dict(request.data)

    if data['status'] == 'initiated':
        return Response(status=200)
    else:
        call = OutgoingCallLog.objects.get(twilio_call_id=data['CallSid'])
        call.status = data['status']
        call.duration = data['duration']
        call.save()
        return Response(status=200)
