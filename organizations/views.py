from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.permissions import HasSessionOrTokenActive
from users.api import get_request_user
from .models import OrgUser, OrgProfile
from .serializers import OrgProfileSerializer
from utils.error_handling.error_message import ErrorMessage
from roles.permissions import HasPermission
from roles.base_permissions import UPDATE_ORGANIZATION


@api_view(['GET'])
@permission_classes([HasSessionOrTokenActive])
def me(request):
    """Get organization profile

    Args:
        request (Request): Request object
    """
    user = get_request_user(request)
    org_user = OrgUser.objects.select_related('organization').get(user=user)
    organization = org_user.organization
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


@api_view(['POST'])
@permission_classes([HasSessionOrTokenActive, HasPermission(UPDATE_ORGANIZATION)])
def createOrUpdateOrgProfile(request):
    """Create or update organization profile

    Args:
        request (Request): Request object
    """
    user = get_request_user(request)
    org_user = OrgUser.objects.select_related('organization').get(user=user)
    organization = org_user.organization
    # Get profile
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
        # Create profile
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
