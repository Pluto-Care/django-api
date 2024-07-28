from django.utils.encoding import force_str
from django.db.models import Q
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from users.serializers import UserSerializer
from utils.error_handling.error_message import ErrorMessage
from roles.permissions import HasPermission
from roles.base_permissions import UPDATE_ORGANIZATION, READ_ALL_USERS, UPDATE_USER_PROFILE
from .api import get_user_org
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
    org_users = OrgUser.objects.select_related(
        'user').filter(organization=organization)
    users = [org_user.user for org_user in org_users]
    return Response(data=UserSerializer(users, many=True).data, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(READ_ALL_USERS)])
def search_org_users(request):
    """
    Search for users in the organization
    """
    organization = get_user_org(get_request_user(request))
    keyword = force_str(request.data['keyword'])
    if keyword is None or keyword == '':
        return ErrorMessage(
            title='Keyword Required',
            detail='Keyword is required.',
            instance=request.build_absolute_uri(),
            status=400,
            code='KeywordRequired',
        ).to_response()
    org_users = OrgUser.objects.select_related('user').filter(
        Q(organization=organization),
        Q(user__first_name__startswith=keyword) | Q(
            user__last_name__startswith=keyword)
    )
    users = [org_user.user for org_user in org_users]
    return Response(data=UserSerializer(users, many=True).data, status=200)


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(UPDATE_USER_PROFILE)])
def update_org_user_profile(request, user_id):
    """
    Update user profile in the organization
    """
    organization = get_user_org(get_request_user(request))
    try:
        org_user = OrgUser.objects.select_related('user').get(
            organization=organization, user__id=user_id)
        data = dict(
            email=force_str(request.data.get('email', org_user.user.email)),
            first_name=force_str(request.data.get(
                'first_name', org_user.user.first_name)),
            last_name=force_str(request.data.get(
                'last_name', org_user.user.last_name)),
            is_active=force_str(request.data.get(
                'is_active', org_user.user.is_active)),
            timezone=force_str(request.data.get(
                'timezone', org_user.user.timezone)),
            updated_by=get_request_user(request).id,
            updated_at=now()
        )
        serializer = UserSerializer(
            org_user.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return ErrorMessage(
            title='Invalid User Profile Update',
            detail=serializer.errors,
            instance=request.build_absolute_uri(),
            status=400,
            code='UserProfileUpdateInvalid',
        ).to_response()
    except OrgUser.DoesNotExist:
        return ErrorMessage(
            title='User Not Found',
            detail='User not found in the organization.',
            instance=request.build_absolute_uri(),
            status=404,
            code='UserNotFound',
        ).to_response()
