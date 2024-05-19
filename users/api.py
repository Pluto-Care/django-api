from .models import User


def get_user(email):
    """
    Get active User object

    Args:
        email (str): User email

    Returns: User or None
    """
    try:
        account = User.objects.get(email=email, is_active=True)
        return account
    except User.DoesNotExist:
        return None
