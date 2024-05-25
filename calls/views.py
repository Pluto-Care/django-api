from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from utils.error_handling.error_message import ErrorMessage
from decouple import config
# Twilio
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from .decorators import validate_twilio_request
# User Imports
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive])
def make_call(request):
    phone_number = request.data.get('phone_number')
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to=phone_number,
        from_=config('TWILIO_PHONE_NUMBER')
    )

    return JsonResponse({"call_id": call.sid}, status=200, safe=False)


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive])
def grant_twilio_token(request):
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
    return HttpResponse(vr.to_xml(), content_type='text/xml')
