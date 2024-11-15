from .models import Organization, OrgUser
from users.api import add_user
from roles.api import assign_permission_to_user
from roles.base_permissions import base_permission


def new_organization(user_email, user_password, user_first_name, user_last_name):
    """
    Create a new organization. This creates a user as well who is the admin of the organization.

    Args:
        user_email (str): User email
        user_password (str): User password
        user_first_name (str): User first name
        user_last_name (str): User last name

    Returns: Organization or None
    """
    # Create user
    user = add_user(user_email, user_password, user_first_name, user_last_name)
    if user:
        # Create organization
        organization = Organization.objects.create_org()
        # Create org user
        OrgUser.objects.create_org_user(organization=organization, user=user)
        # Assign permission to user
        assign_permission_to_user(user, base_permission['FULL_ACCESS'])
        return organization
    else:
        return None


def get_user_org(user):
    """
    Get user's organization

    Args:
        user (User): User object

    Returns: Organization or None
    """
    try:
        org_user = OrgUser.objects.select_related(
            'organization').get(user=user)
        return org_user.organization
    except OrgUser.DoesNotExist:
        return None


def get_org_user(user, organization):
    """
    Get organization user

    Args:
        user (User): User
        organization (Organization): Organization object

    Returns: User or None
    """
    try:
        org_user = OrgUser.objects.select_related(
            'user').get(user=user, organization=organization)
        return org_user.user
    except OrgUser.DoesNotExist:
        return None


def get_org_user_from_id(user_id, organization):
    """
    Get organization user

    Args:
        user_id (string): User ID
        organization (Organization): Organization object

    Returns: User or None
    """
    try:
        org_user = OrgUser.objects.select_related(
            'user').get(user_id=user_id, organization=organization)
        return org_user.user
    except OrgUser.DoesNotExist:
        return None
