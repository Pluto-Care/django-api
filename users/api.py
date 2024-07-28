from .models import User
from core.middlewares import is_web
# Session Imports
from .users_sessions.utils import get_active_session
# App Token Imports
from .users_app_tokens.utils import get_active_token
from .serializers import UserSerializer


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


def get_request_user(request):
    if is_web(request):
        # Check if session is active
        session = get_active_session(request)
        if session is not None:
            return session.user
    # Check if token is active
    app_token = get_active_token(request)
    if app_token is not None:
        return app_token.user
    return None


def add_user(email, password, first_name, last_name, created_by=None, serialized=False):
    """
    Add a new User

    Args:
        email (str): User email
        password (str): User password
        first_name (str): User first name
        last_name (str): User last name
        created_by (User, optional): User object. Defaults to None.
        serialized (bool, optional): Return serialized User. Defaults to False.

    Returns: User or None
    """
    try:
        account = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            created_by=created_by
        )
        if serialized:
            return UserSerializer(data=account).data
        else:
            return account
    except Exception as e:
        raise Exception(e)


def change_password(user, new_password):
    """
    Change user password

    Args:
        user (User): User object
        new_password (str): New password

    Returns: User or None
    """
    try:
        user.set_password(new_password)
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def change_email(user, new_email):
    """
    Change user email

    Args:
        user (User): User object
        new_email (str): New email

    Returns: User or None
    """
    try:
        user.email = new_email
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def change_name(user, new_first_name, new_last_name):
    """
    Change user name

    Args:
        user (User): User object
        new_first_name (str): New first name
        new_last_name (str): New last name

    Returns: User or None
    """
    try:
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def disable_user(user: User):
    """
    Disable user

    Args:
        user (User): User object

    Returns: User or None
    """
    try:
        user.is_active = False
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def enable_user(user):
    """
    Enable user

    Args:
        user (User): User object

    Returns: User or None
    """
    try:
        user.is_active = True
        user.save()
        return user
    except Exception as e:
        raise Exception(e)


def delete_user(user):
    """
    Delete user

    Args:
        user (User): User object

    Returns: User or None
    """
    try:
        user.delete()
        return user
    except Exception as e:
        raise Exception(e)
