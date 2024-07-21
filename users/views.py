from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from utils.error_handling.error_message import ErrorMessage
from decouple import config
from core.middlewares import is_web
from core.settings import SECRET_KEY
# JWT
import jwt
# Session Imports
from .users_sessions.api import create_session, delete_session, get_last_session_details
from .users_sessions.utils import get_active_session
# App Token Imports
from .users_app_tokens.api import create_app_token, get_last_token_session_details, delete_app_token
from .users_app_tokens.utils import get_active_token
# TOTP Imports
from .users_totp.api import has_totp, authenticate_totp, create_mfa_join_token
# User Imports
from .serializers import UserSerializer, LoginSerializer
from .permissions import HasSessionOrTokenActive
# Roles Imports
from roles.api import get_user_permissions, get_user_role


@api_view(['POST'])
def login(request):
    # Validate request data
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Get user
        user = serializer.validated_data
        # Check if user hash TOTP enabled
        totp_row = has_totp(user)
        if totp_row is not None:
            # If token is not provided
            if 'token' not in request.data or ('token' in request.data and (request.data['token'] == None or request.data['token'] == '')):
                return ErrorMessage(
                    detail="TOTP token is required.",
                    status=401,
                    instance=request.build_absolute_uri(),
                    title='2FA code is required',
                    code='TOTPRequired'
                ).to_response()
            # Authenticate TOTP
            if not authenticate_totp(user, force_str(request.data['token']), totp_row):
                return ErrorMessage(
                    detail="Provided TOTP code or backup code is incorrect. Please try again.",
                    status=401,
                    instance=request.build_absolute_uri(),
                    title='2FA code is incorrect',
                    code='TOTPIncorrect'
                ).to_response()
        else:
            # TODO: commented out for development purposes
            # Create a MFA Join Token
            mfa_join_token, _ = create_mfa_join_token(user, request)
            response = Response(
                data={
                    "mfa_join_token": mfa_join_token,
                    "detail": "MFA is required.",
                    "reason": "MFA_REQUIRED"
                },
                status=202
            )
            return response
        # Get last session details
        last_session = get_last_session_details(user)  # already serialized
        last_token_session = get_last_token_session_details(
            user)  # already serialized
        # Get roles and permissions
        role = get_user_role(user)
        permissions = get_user_permissions(user)
        # Respond depending on the client
        if is_web(request):
            # Session based authentication
            key, session = create_session(user, request)
            # Add HTTPOnly cookie
            response = Response(data={
                "last_session": last_session,
                "last_token_session": last_token_session,
                "permissions": permissions,
                "role": role,
                "user": UserSerializer(user).data
            },
                status=200
            )
            response.set_cookie(
                key=config('AUTH_COOKIE_NAME', default='auth'),
                value=jwt.encode(
                    {
                        "session_key": key
                    },
                    SECRET_KEY,
                    algorithm='HS256'
                ),
                expires=session.expire_at,
                httponly=True,
                secure=config('AUTH_COOKIE_SECURE', default=True, cast=bool),
                samesite=config('AUTH_COOKIE_SAMESITE', default='Strict'),
                domain=config('AUTH_COOKIE_DOMAIN', default='localhost')
            )
            return response
        else:
            # Token based authentication
            token, app_token = create_app_token(user, request)
            # Respond with token and user data
            return Response(data={
                "last_session": last_session,
                "last_token_session": last_token_session,
                "permissions": permissions,
                "role": role,
                "user": UserSerializer(user).data,
                "session": dict(
                    id=app_token.id,
                    key=jwt.encode(
                        {
                            "app_token": token
                        },
                        SECRET_KEY,
                        algorithm='HS256'
                    ),
                )
            },
                status=200
            )
    errors = serializer.errors
    err_msg = ErrorMessage(
        detail=errors,
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid credentials',
        code='LoginSerializedErrors'
    )
    return err_msg.to_response()


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive])
def logout(request):
    # Delete session or token
    if is_web(request):
        delete_session(get_active_session(request).user,
                       get_active_session(request).id)
        response = Response(status=200)
        response.delete_cookie(
            key=config('AUTH_COOKIE_NAME', default='auth'),
            domain=config('AUTH_COOKIE_DOMAIN', default='localhost')
        )
        return response
    else:
        delete_app_token(get_active_token(request).user,
                         get_active_token(request).id)
    # Return response
    return Response(status=200)


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive])
def me(request):

    # Session-based authentication
    if is_web(request):
        session = get_active_session(request)
        role = get_user_role(session.user)
        permissions = get_user_permissions(session.user)
        if session is not None:
            return Response(data=dict(
                user=UserSerializer(session.user).data,
                role=role,
                permissions=permissions
            ), status=200)
    # Token-based authentication
    app_token = get_active_token(request)
    role = get_user_role(app_token.user)
    permissions = get_user_permissions(app_token.user)
    if app_token is not None:
        return Response(data=dict(
            user=UserSerializer(app_token.user).data,
            role=role,
            permissions=permissions
        ), status=200)
    # No valid active session or token found
    return ErrorMessage(
        detail='No active session or token found.',
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid request',
        code='NoActiveSessionOrToken'
    ).to_response()
