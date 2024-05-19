from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from decouple import config
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.error_handling.error_message import ErrorMessage
from users.serializers import PasswordSerializer
from users.users_utils.emailing.api import send_forgot_password_email, send_password_changed_email
from .models import ForgotPassword
from .serializers import HealthyForgotPasswordSerializer
from .utils import KEY_LENGTH


@api_view(['POST'])
def forgot_password(request):
    # Check if all required fields are provided
    if 'email' not in request.data:
        err = ErrorMessage(
            title='Email is required.',
            status=400,
            detail='Email is required.',
            instance=request.get_full_path(),
        )
        return err.to_response()
    key, fp = ForgotPassword.objects.create_forgot_password(
        request,
        force_str(request.data['email'])
    )
    if key and fp:
        key = urlsafe_base64_encode(key.encode("ascii"))
        # Send email with key
        url = f'{config("FRONTEND_URL")}/api_action/user/forgot_password/{urlsafe_base64_encode(key.encode("ascii"))}/'
        send_forgot_password_email(
            email=force_str(fp.user.email),
            reset_url=url,
            first_name=fp.user.first_name,
            subject='Reset your password'
        )
    # Send empty success response
    return Response(status=204)


@api_view(['POST'])
def check_health(request):
    key = force_str(request.data['key'])
    key = urlsafe_base64_decode(key).decode("ascii")
    serializer = HealthyForgotPasswordSerializer(data={'key': key})
    if not serializer.is_valid():
        err = ErrorMessage(
            title='Invalid Request',
            status=400,
            detail=serializer.errors,
            instance=request.get_full_path(),
        )
        return err.to_response()
    # Send empty success response
    return Response(status=204)


@api_view(['POST'])
def reset_password(request):
    # Check if password is provided
    if 'password' not in request.data:
        err = ErrorMessage(
            title='Password Required',
            status=400,
            detail='Password is required.',
            instance=request.get_full_path(),
        )
        return err.to_response()
    # Check if key is permissible
    key = force_str(request.data['key'])
    key = urlsafe_base64_decode(key).decode("ascii")
    if len(key) != KEY_LENGTH:
        err = ErrorMessage(
            title='Invalid Request',
            status=400,
            detail='URL or key is invalid. Please request a new password reset.',
            instance=request.get_full_path(),
        )
        return err.to_response()
    # Check if key is valid
    serializer = HealthyForgotPasswordSerializer(data={'key': key})
    if not serializer.is_valid():
        err = ErrorMessage(
            title='Invalid Request',
            status=400,
            detail=serializer.errors,
            instance=request.get_full_path(),
        )
        return err.to_response()
    fp = serializer.validated_data
    # Validate password
    serializer = PasswordSerializer(data=request.data)
    if serializer.is_valid():
        # Set new password
        fp.user.set_password(force_str(request.data['password']))
        fp.user.save()
        # Set fp as used
        fp.set_used()
        # Send notification email to user
        send_password_changed_email(
            email=fp.user.email,
            first_name=fp.user.first_name,
            subject='Password Changed'
        )
        # Send empty success response
        return Response(status=204)
    else:
        err = ErrorMessage(
            title='Encountered Error',
            status=400,
            detail=serializer.errors,
            instance=request.get_full_path(),
        )
        return err.to_response()
