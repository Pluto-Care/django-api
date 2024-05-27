from django.utils.encoding import force_str
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.permissions import HasSessionOrTokenActive
from .models import Totp, MFAJoinToken
from .permissions import HasMFAJoinToken
from users.users_utils.active_user import get_active_user


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive | HasMFAJoinToken])
def totp_init(request):
    app_name = 'Pluto%20Health'
    # Get user
    user = get_active_user(request)
    if user is None:
        mfa_join_token = MFAJoinToken.objects.verify_token(
            request.data['mfa_join_token'], request)
        if mfa_join_token is None:
            return Response(data={'detail': 'Invalid MFA Join Token', 'code': 'U-TOTP400'}, status=400)
        user = mfa_join_token.user
    # Create TOTP
    new_totp = Totp.objects.create_totp(user)
    if new_totp is None:
        return Response(data={'detail': 'TOTP is already enabled', 'code': 'U-TOTP401'}, status=400)
    key, backup_codes, _ = new_totp
    return Response(data={
        'key': key,
        'backup_codes': backup_codes,
        'provision': f"otpauth://totp/{app_name}:{user.email.replace('@','%40')}?secret={key}&issuer={app_name}"
    }, status=201)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive | HasMFAJoinToken])
def totp_enable(request):
    """ Enable TOTP for the user after user initiates the TOTP.

    Request Parameters:
        token (str): 6 len OTP code only
    """
    token = force_str(request.data.get('token'))
    # If backup code is being used, then return 400 right away
    if len(token) > 6:
        return Response(data={'detail': 'Invalid token', 'code': 'U-TOTP400'}, status=400)
    # Try to authenticate the user
    try:
        # Get user
        user = get_active_user(request)
        if user is None:
            mfa_join_token = MFAJoinToken.objects.verify_token(
                request.data['mfa_join_token'], request)
            if mfa_join_token is None:
                return Response(data={'detail': 'Invalid MFA Join Token', 'code': 'U-TOTP400'}, status=400)
            user = mfa_join_token.user
        # If authenticated, totp object will be returned otherwise None
        totp = Totp.objects.authenticate(user, token)
        # Only enable if the status is initialized
        # Disabled totp's cannot be enabled again
        if totp:
            if totp.status == 'initialized':
                totp.status = 'enabled'
                totp.save()
                MFAJoinToken.objects.consume_token(
                    request.data['mfa_join_token'])
            return Response(status=204)
        return Response(data={'detail': 'Invalid token', 'code': 'U-TOTP400'}, status=400)
    except Totp.DoesNotExist:
        return Response(data={'detail': 'TOTP not set', 'code': 'U-TOTP404'}, status=400)


@api_view(['PUT'])
@permission_classes([HasSessionOrTokenActive])
def totp_disable(request):
    """ Disable TOTP for the user.

    Request Parameters:
        token (str): 6 len OTP code or 8 len backup code
    """
    # Get the token from request
    token = force_str(request.data.get('token'))
    # Try to authenticate the user
    try:
        totp = Totp.objects.authenticate(get_active_user(request), token)
    except Totp.DoesNotExist:
        return Response(data={'detail': 'Invalid token', 'code': 'U-TOTP400'}, status=400)
    if totp:
        totp.status = 'disabled'
        totp.updated_at = now()
        totp.save()
        return Response(status=204)
    return Response(data={'detail': 'Invalid token. Cannot disable TOTP.', 'code': 'U-TOTP400'}, status=400)


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive])
def totp_new_backup_codes(request):
    """
    Generate new backup codes for the user. Invalidates the old backup codes.
    """
    # TODO: Require TOTP token to generate new backup codes
    # to prevent fraudalent activities

    # Create new backup codes
    backup_codes = Totp.objects.create_new_backup_codes(
        get_active_user(request))
    if backup_codes is None:
        return Response(data={'detail': 'TOTP not set.', 'code': 'U-TOTP404'}, status=400)
    return Response(data={'backup_codes': backup_codes}, status=200)
