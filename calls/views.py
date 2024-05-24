from django.db import IntegrityError
from django.utils.encoding import force_str
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from utils.error_handling.error_message import ErrorMessage
from decouple import config
from core.middlewares import is_web
# Twilio
from twilio import twiml
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
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

    token = AccessToken(account_sid, api_key, api_secret,
                        identity=get_request_user(request).email,
                        ttl=3600)

    # add grants to token
    token.add_grant(VoiceGrant(incoming_allow=True,
                    push_credential_sid=config('TWILIO_PUSH_CREDENTIAL_SID'),
                    outgoing_application_sid=config(
                        'TWILIO_OUTGOING_APPLICATION_SID')
    ))

    return JsonResponse({"token": token.to_jwt()}, status=200, safe=False)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive])
def twiml(request):
    voice_response = twiml.VoiceResponse()

    if not hasattr(request.data, 'to'):
        return Response(ErrorMessage('to is required'), status=400)

    print(request.data)

    return Response(status=400)
