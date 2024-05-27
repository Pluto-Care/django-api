from .models import Organization, OrgUser
from users.api import add_user


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
