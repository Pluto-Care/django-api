from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user, add_user, change_password, disable_user, enable_user, get_user_password_change
from users.serializers import UserSerializer, AddUserSerializer, PasswordSerializer, UserPasswordChangeSerializer
from users.users_totp.api import disable_totp
from users.models import UserPasswordChange
from utils.error_handling.error_message import ErrorMessage
from roles.permissions import HasPermission
from roles.base_permissions import READ_ALL_USERS, CREATE_NEW_USER, UPDATE_USER_PASSWORD, UPDATE_USER_MFA, DISABLE_USER, ENABLE_USER
from roles.api import get_user_role, get_user_permissions
from .api import get_user_org, get_org_user_from_id
from .models import OrgUser


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(CREATE_NEW_USER)])
def create_org_user(request):
    """
    Create a new user in the organization
    """
    organization = get_user_org(get_request_user(request))
    serializer = AddUserSerializer(data=request.data)
    if serializer.is_valid() is False:
        return ErrorMessage(
            title='Invalid User Creation',
            detail=serializer.errors,
            instance=request.build_absolute_uri(),
            status=400,
            code='UserCreationInvalid',
        ).to_response()
    user = add_user(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
        first_name=serializer.validated_data['first_name'],
        last_name=serializer.validated_data['last_name'],
        created_by=get_request_user(request)
    )
    if user:
        OrgUser.objects.create_org_user(organization=organization, user=user)
        return Response(UserSerializer(user).data, status=201)
    return ErrorMessage(
        title='Invalid User Creation',
        detail='User creation failed.',
        instance=request.build_absolute_uri(),
        status=400,
        code='UserCreationInvalid',
    ).to_response()


class OrgUserView(APIView):
    """
    Get user details for admin users
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [HasSessionOrTokenActive(), HasPermission(READ_ALL_USERS)]
        return [False]

    def get(self, request, *args, **kwargs):
        """
        Get user details
        """
        user_id = self.kwargs.get('user_id')
        if user_id is None:
            return ErrorMessage(
                title='User ID Required',
                detail='User ID is required.',
                instance=request.build_absolute_uri(),
                status=400,
                code='UserIDRequired',
            ).to_response()
        organization = get_user_org(get_request_user(request))
        try:
            org_user = OrgUser.objects.select_related('user', 'user__created_by', 'user__updated_by').get(
                user_id=user_id, organization=organization)
            pswd_change_row = get_user_password_change(org_user.user)
            return Response(
                dict(
                    user=UserSerializer(org_user.user).data,
                    role=get_user_role(org_user.user),
                    permissions=get_user_permissions(org_user.user),
                    created_by=UserSerializer(
                        org_user.user.created_by).data if org_user.user.created_by else None,
                    updated_by=UserSerializer(
                        org_user.user.updated_by).data if org_user.user.updated_by else None,
                    password_change=UserPasswordChangeSerializer(
                        pswd_change_row).data if pswd_change_row else None
                ),
                status=200)
        except OrgUser.DoesNotExist:
            return ErrorMessage(
                title='User Not Found',
                detail='User not found.',
                instance=request.build_absolute_uri(),
                status=404,
                code='UserNotFound',
            ).to_response()


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(UPDATE_USER_PASSWORD)])
def reset_org_user_password(request, user_id):
    """
    Admins resetting a user password
    """
    org = get_user_org(get_request_user(request))
    user = get_org_user_from_id(user_id, org)
    if user:
        new_password = force_str(request.data.get('new_password'))
        serializer = PasswordSerializer(data={'password': new_password})
        if serializer.is_valid() is False:
            return ErrorMessage(
                title='Invalid Password',
                detail=serializer.errors,
                instance=request.build_absolute_uri(),
                status=400,
                code='PasswordInvalid',
            ).to_response()
        try:
            change_password(user, new_password)
            UserPasswordChange.objects.save_due_change_by_admin(
                user, get_request_user(request))
        except Exception as e:
            return ErrorMessage(
                title='Password Reset Failed',
                detail=str(e),
                instance=request.build_absolute_uri(),
                status=400,
                code='PasswordResetFailed',
            ).to_response()
        return Response(data={'message': 'The password has been reset'}, status=200)
    return ErrorMessage(
        title='User Not Found',
        detail='User not found.',
        instance=request.build_absolute_uri(),
        status=404,
        code='UserNotFound',
    ).to_response()


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(UPDATE_USER_MFA)])
def disable_org_user_mfa(request, user_id):
    """
    Admins disabling a user MFA
    """
    org = get_user_org(get_request_user(request))
    user = get_org_user_from_id(user_id, org)
    if user:
        disable_totp(user)
        return Response(data={'message': 'The MFA has been disabled'}, status=200)
    return ErrorMessage(
        title='User Not Found',
        detail='User not found.',
        instance=request.build_absolute_uri(),
        status=404,
        code='UserNotFound',
    ).to_response()


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(DISABLE_USER)])
def disable_org_user_account(request, user_id):
    """
    Admins disabling a user account
    """
    org = get_user_org(get_request_user(request))
    user = get_org_user_from_id(user_id, org)
    if user:
        disable_user(user)
        return Response(data={'message': 'The account has been disabled'}, status=200)
    return ErrorMessage(
        title='User Not Found',
        detail='User not found.',
        instance=request.build_absolute_uri(),
        status=404,
        code='UserNotFound',
    ).to_response()


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(ENABLE_USER)])
def enable_org_user_account(request, user_id):
    """
    Admins enabling a user account
    """
    org = get_user_org(get_request_user(request))
    user = get_org_user_from_id(user_id, org)
    if user:
        enable_user(user)
        return Response(data={'message': 'The account has been enabled'}, status=200)
    return ErrorMessage(
        title='User Not Found',
        detail='User not found.',
        instance=request.build_absolute_uri(),
        status=404,
        code='UserNotFound',
    ).to_response()
