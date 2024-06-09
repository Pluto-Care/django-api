from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user, add_user
from users.serializers import UserSerializer, AddUserSerializer
from utils.error_handling.error_message import ErrorMessage
from roles.permissions import HasPermission
from roles.base_permissions import UPDATE_ORGANIZATION, READ_ALL_USERS, CREATE_NEW_USER
from .api import get_user_org, get_org_user
from .models import OrgUser, OrgProfile
from .serializers import OrgProfileSerializer


class OrgProfileView(APIView):
    """
    Create, get or update organization profile. The user requesting can only access
    their own organization profile.
    """

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [HasSessionOrTokenActive(), HasPermission(UPDATE_ORGANIZATION)]
        if self.request.method == 'POST':
            return [HasSessionOrTokenActive(), HasPermission(UPDATE_ORGANIZATION)]
        elif self.request.method == 'GET':
            return [HasSessionOrTokenActive()]
        return [False]

    def get(self, request, *args, **kwargs):
        """
        Get organization profile
        """
        organization = get_user_org(get_request_user(request))
        if organization is None:
            return ErrorMessage(
                title='Organization Not Found',
                detail='Organization not found.',
                instance=request.build_absolute_uri(),
                status=404,
                code='OrgNotFound',
            ).to_response()
        # Get profile
        try:
            org_profile = OrgProfile.objects.get(organization=organization)
            serializer = OrgProfileSerializer(org_profile)
            return Response(serializer.data, status=200)
        except OrgProfile.DoesNotExist:
            return ErrorMessage(
                title='Organization Profile Not Found',
                detail='Organization profile not found.',
                instance=request.build_absolute_uri(),
                status=404,
                code='OrgProfileNotFound',
            ).to_response()

    def put(self, request, *args, **kwargs):
        """
        Update organization profile
        """
        organization = get_user_org(get_request_user(request))
        if organization is None:
            return ErrorMessage(
                title='Organization Not Found',
                detail='Organization not found.',
                instance=request.build_absolute_uri(),
                status=404,
                code='OrgNotFound',
            ).to_response()
        try:
            org_profile = OrgProfile.objects.get(organization=organization)
            # Update profile
            serializer = OrgProfileSerializer(
                org_profile, data={**request.data, 'organization': organization.id}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return ErrorMessage(
                title='Invalid Organization Profile Update',
                detail=serializer.errors,
                instance=request.build_absolute_uri(),
                status=400,
                code='OrgProfileUpdateInvalid',
            ).to_response()
        except OrgProfile.DoesNotExist:
            return ErrorMessage(
                title='Organization Profile Not Found',
                detail='Organization profile not found.',
                instance=request.build_absolute_uri(),
                status=404,
                code='OrgProfileNotFound',
            ).to_response()

    def post(self, request, *args, **kwargs):
        """
        Create organization profile
        """
        organization = get_user_org(get_request_user(request))
        # Check if org exist
        if organization is not None:
            return ErrorMessage(
                title='Organization Already Exists',
                detail='Organization already exists.',
                instance=request.build_absolute_uri(),
                status=400,
                code='OrgAlreadyExists',
            ).to_response()
        # Check if org profile already exist
        org_profile_exists = OrgProfile.objects.filter(
            organization=organization).exists()
        if org_profile_exists:
            return ErrorMessage(
                title='Organization Profile Already Exists',
                detail='Organization profile already exists.',
                instance=request.build_absolute_uri(),
                status=400,
                code='OrgProfileAlreadyExists',
            ).to_response()
        # Create new org profile
        serializer = OrgProfileSerializer(
            data={**request.data, 'organization': organization.id})
        if serializer.is_valid():
            serializer.save(organization=organization)
            return Response(serializer.data, status=201)
        return ErrorMessage(
            title='Invalid Organization Profile Creation',
            detail=serializer.errors,
            instance=request.build_absolute_uri(),
            status=400,
            code='OrgProfileCreationInvalid',
        ).to_response()


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive, HasPermission(READ_ALL_USERS)])
def get_org_users(request):
    """
    Get all users in the organization
    """
    organization = get_user_org(get_request_user(request))
    if organization is None:
        return ErrorMessage(
            title='Organization Not Found',
            detail='Organization not found.',
            instance=request.build_absolute_uri(),
            status=404,
            code='OrgNotFound',
        ).to_response()
    org_users = OrgUser.objects.select_related(
        'user').filter(organization=organization)
    users = [org_user.user for org_user in org_users]
    return Response(data=UserSerializer(users, many=True).data, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(CREATE_NEW_USER)])
def create_org_user(request):
    """
    Create a new user in the organization
    """
    organization = get_user_org(get_request_user(request))
    if organization is None:
        return ErrorMessage(
            title='Organization Not Found',
            detail='Organization not found.',
            instance=request.build_absolute_uri(),
            status=404,
            code='OrgNotFound',
        ).to_response()
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
        last_name=serializer.validated_data['last_name']
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
    Get user details
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [HasSessionOrTokenActive()]
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
        user = get_org_user(user_id, organization)
        if user:
            return Response(UserSerializer(user).data, status=200)
        return ErrorMessage(
            title='User Not Found',
            detail='User not found.',
            instance=request.build_absolute_uri(),
            status=404,
            code='UserNotFound',
        ).to_response()
