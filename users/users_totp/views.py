from django.utils.encoding import force_str
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.permissions import HasSessionOrTokenActive
from .models import Totp, MFAJoinToken
from .permissions import HasMFAJoinToken
from users.users_utils.active_user import get_active_user
from utils.error_handling.error_message import ErrorMessage


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
            return ErrorMessage(
                title='Invalid MFA Join Token',
                detail='Please login again to continue. Previous session is likely expired.',
                status=400,
                code='InvalidMFAJoinToken',
                instance=request.build_absolute_uri()
            ).to_response()
        user = mfa_join_token.user
    # Create TOTP
    new_totp = Totp.objects.create_totp(user)
    if new_totp is None:
        return ErrorMessage(
            title='TOTP is already enabled',
            detail='You are attempting to setup TOTP but it is already enabled.',
            status=400,
            code='TOTPAlreadyEnabledOnInit',
            instance=request.build_absolute_uri()
        ).to_response()
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
        return ErrorMessage(
            title='Invalid TOTP Token',
            detail='Please use a 6-digit TOTP token to enable TOTP. Backup codes cannot be used.',
            status=400,
            code='InvalidTOTPTokenTooLong',
            instance=request.build_absolute_uri()
        ).to_response()
    # Try to authenticate the user
    try:
        # Get user
        user = get_active_user(request)
        if user is None:
            mfa_join_token = MFAJoinToken.objects.verify_token(
                request.data['mfa_join_token'], request)
            if mfa_join_token is None:
                return ErrorMessage(
                    title='Invalid MFA Join Token',
                    detail='Please login again to continue. Previous session is likely expired.',
                    status=400,
                    code='InvalidMFAJoinToken',
                    instance=request.build_absolute_uri()
                ).to_response()
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
            return Response(status=200)
        return ErrorMessage(
            title='Invalid TOTP Token',
            detail='The provided TOTP token is invalid. Please try again.',
            status=400,
            code='InvalidTOTPToken',
            instance=request.build_absolute_uri()
        ).to_response()
    except Totp.DoesNotExist:
        return ErrorMessage(
            title='TOTP not set',
            detail='You will need to start the TOTP setup process first.',
            status=400,
            code='TOTPNotSetup',
            instance=request.build_absolute_uri()
        ).to_response()


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
    totp = Totp.objects.authenticate(get_active_user(request), token)
    if totp:
        totp.status = 'disabled'
        totp.updated_at = now()
        totp.save()
        return Response(status=200)
    return ErrorMessage(
        title='Invalid TOTP Token',
        detail='The provided TOTP token or backup code is invalid. Please try again.',
        status=400,
        code='InvalidTOTPToken',
        instance=request.build_absolute_uri()
    ).to_response()


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
        return ErrorMessage(
            title='TOTP not set',
            detail='You will need to start the TOTP setup process first.',
            status=400,
            code='TOTPNotSetup',
            instance=request.build_absolute_uri()
        ).to_response()
    return Response(data={'backup_codes': backup_codes}, status=200)
