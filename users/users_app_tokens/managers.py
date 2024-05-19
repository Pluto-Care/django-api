import uuid
from django.db import models
from django.utils.timezone import now
from .utils import generate_token, hash_this, getClientIP, getUserAgent
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class AppTokenManager(models.Manager):

    def __init__(self):
        super().__init__()

    def create_app_token(self, user, request):
        """Primary use case: Create a app token on login for Authorization header

        Args:
            user (User): User to create app_token for
            request (HttpRequest): For IP and User-Agent

        Returns:
            tuple(key: str, token: Token)
        """
        # Disable previous sessions from same IP and User-Agent
        self.filter(user=user, ip=getClientIP(request),
                    ua=getUserAgent(request), is_valid=True).update(is_valid=False)
        key = generate_token()
        token = self.create(
            id=uuid.uuid4(),
            user=user,
            token=hash_this(key),
            ip=getClientIP(request),
            ua=getUserAgent(request),
        )
        return urlsafe_base64_encode(key.encode("ascii")), token

    def delete_app_token(self, user, app_token_id):
        """Primary use case: Logout a user

        Args:
            user (User): Model object
            app_token_id (uuid): The row id of the app_token
        """
        try:
            app_token = self.get(user=user, id=app_token_id, is_valid=True)
            if app_token.is_valid:
                app_token.is_valid = False
                app_token.updated_at = now()
                app_token.save()
        except Exception as e:
            return None
        return None

    def authenticate_app_token(self, token, ua):
        """This function authenticates a user request

        Args:
            token (str): App token from Authorization header

        Returns:
            AppToken or None
        """
        try:
            key = urlsafe_base64_decode(token).decode("ascii")
            app_token = self.select_related('user').get(
                token=hash_this(key),
                ua=ua,
                is_valid=True
            )
            if not app_token.is_valid:
                return None
            return app_token
        except Exception as e:
            return None

    def get_app_token_if_valid(self, user, app_token_id):
        """Get app_token if it is valid and not expired.

        Args:
            user (User): User model object
            app_token_id (int): Session row id

        Returns:
            Session or None
        """
        try:
            app_token = self.select_related('user').get(
                user=user,
                id=app_token_id,
                is_valid=True
            )
            return app_token
        except Exception as e:
            return None

    def get_last_session(self, user):
        return self.filter(user=user).order_by('-created_at').first()

    def get_user(self, app_token_id):
        try:
            return self.get(id=app_token_id).user
        except Exception as e:
            return None
