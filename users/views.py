from django.db import IntegrityError
from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from utils.error_handling.error_message import ErrorMessage
from decouple import config
# Session Imports
from .users_sessions.api import create_session, delete_session, get_last_session_details
from .users_sessions.utils import get_active_session
# App Token Imports
from .users_app_tokens.api import create_app_token, get_last_token_session_details
# TOTP Imports
from .users_totp.api import has_totp, authenticate_totp
# User Imports
from .models import User
from .serializers import UserSerializer, LoginSerializer
from .permissions import HasSessionActive


@api_view(['POST'])
def signup(request):
    # Validate request data
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Create user
        try:
            user = User.objects.create_user(**serializer.validated_data)
            return Response(data=UserSerializer(user).data, status=201)
        except IntegrityError:
            return ErrorMessage(
                detail='User with this email already exists.',
                status=400,
                instance=request.build_absolute_uri(),
                title='Invalid data provided'
            ).to_response()
    errors = serializer.errors
    err_msg = ErrorMessage(
        detail=errors,
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid data provided'
    )
    return err_msg.to_response()


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
            if 'token' not in request.data:
                return ErrorMessage(
                    detail="TOTP token is required.",
                    status=400,
                    instance=request.build_absolute_uri(),
                    title='Invalid credentials',
                ).to_response()
            # Authenticate TOTP
            if not authenticate_totp(user, force_str(request.data['token']), totp_row):
                return ErrorMessage(
                    detail="TOTP is invalid.",
                    status=400,
                    instance=request.build_absolute_uri(),
                    title='Invalid credentials',
                ).to_response()
        # Get last session details
        last_session = get_last_session_details(user)  # already serialized
        last_token_session = get_last_token_session_details(
            user)  # already serialized
        # Start session
        key, session = create_session(user, request)
        response = Response(data={
            "last_session": last_session,
            "last_token_session": last_token_session,
            "user": UserSerializer(user).data
        },
            status=200
        )
        # Add HTTPOnly cookie
        response.set_cookie(
            key=config('AUTH_COOKIE_NAME', default='auth'),
            value=key,
            expires=session.expire_at,
            httponly=True,
            secure=config('AUTH_COOKIE_SECURE', default=True, cast=bool),
            samesite=config('AUTH_COOKIE_SAMESITE', default='Strict'),
            domain=config('AUTH_COOKIE_DOMAIN', default='localhost')
        )
        return response
    errors = serializer.errors
    err_msg = ErrorMessage(
        detail=errors,
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid credentials',
    )
    return err_msg.to_response()


@api_view(['POST'])
@permission_classes([HasSessionActive])
def logout(request):
    # Delete session
    delete_session(get_active_session(request).user,
                   get_active_session(request).id)
    # Return response
    return Response(status=204)


@api_view(['POST'])
def token_login(request):
    # Validate request data
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Get user
        user = serializer.validated_data
        # Check if user hash TOTP enabled
        totp_row = has_totp(user)
        if totp_row is not None:
            # If token is not provided
            if 'token' not in request.data:
                return ErrorMessage(
                    detail="TOTP token is required.",
                    status=400,
                    instance=request.build_absolute_uri(),
                    title='Invalid credentials',
                ).to_response()
            # Authenticate TOTP
            if not authenticate_totp(user, force_str(request.data['token']), totp_row):
                return ErrorMessage(
                    detail="TOTP is invalid.",
                    status=400,
                    instance=request.build_absolute_uri(),
                    title='Invalid credentials',
                ).to_response()
        # Get last session details
        last_session = get_last_session_details(user)  # already serialized
        last_token_session = get_last_token_session_details(
            user)  # already serialized
        # Start session
        key, session = create_app_token(user, request)
        # Send token and user data
        return Response(data={
            "last_session": last_session,
            "last_token_session": last_token_session,
            "token": key,
            "user": UserSerializer(user).data
        },
            status=200
        )
    errors = serializer.errors
    err_msg = ErrorMessage(
        detail=errors,
        status=400,
        instance=request.build_absolute_uri(),
        title='Invalid credentials',
    )
    return err_msg.to_response()
