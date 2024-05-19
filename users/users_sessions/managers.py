import uuid
from django.db import models
from django.utils.timezone import now
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from datetime import timedelta
from .utils import generate_session_key, hash_this, getClientIP, getUserAgent


class SessionManager(models.Manager):
    """Manages the sessions for the users
    - Create a session: Key generation and expiry
    - Delete a session: Invalidating sessions
    - Get a session: Retrieve a session by key, user, or id
    """

    def __init__(self):
        super().__init__()
        # Session expiry in days
        self.KEY_EXPIRE_IN_DAYS = 30
        # Refresh the session before it expires during authentication
        self.KEY_REFERSH_IN_DAYS = 14

    def create_session(self, user, request):
        """Primary use case: Create a session on signup/login

        Args:
            user (User): User to create session for
            request (HttpRequest): For IP and User-Agent

        Returns:
            tuple(key: str, session: Session)
        """
        # Disable previous sessions from same IP and User-Agent
        self.filter(user=user, ip=getClientIP(request),
                    ua=getUserAgent(request), is_valid=True).update(is_valid=False)
        # Create a new session
        key = generate_session_key()
        session = self.create(
            id=uuid.uuid4(),
            user=user,
            key=hash_this(key),
            ip=getClientIP(request),
            ua=getUserAgent(request),
            expire_at=now() + timedelta(days=self.KEY_EXPIRE_IN_DAYS)
        )
        return urlsafe_base64_encode(key.encode("ascii")), session

    def delete_session(self, user, session_id):
        """Primary use case: Logout a user

        Args:
            user (User): Model object
            session_id (uuid): The row id of the session
        """
        try:
            session = self.get(user=user, id=session_id, is_valid=True)
            if session.is_valid:
                session.is_valid = False
                session.updated_at = now()
                session.save()
        except Exception as e:
            return None
        return None

    def authenticate_session(self, key, ip, ua):
        """This function authenticates a user request

        Args:
            key (str): Session key

        Returns:
            Session or None
        """
        try:
            key = urlsafe_base64_decode(key).decode("ascii")
            session = self.select_related('user').get(
                key=hash_this(key),
                ip=ip,
                ua=ua,
                is_valid=True
            )
            if not session.is_valid:
                return None
            if session.expire_at < now():
                session.is_valid = False
                session.updated_at = now()
                session.save()
                return None
            elif session.expire_at + timedelta(days=self.KEY_REFERSH_IN_DAYS) < now():
                # If the session is about to expire, refresh it
                session.expire_at = now() + timedelta(days=self.KEY_EXPIRE_IN_DAYS)
                session.updated_at = now()
                session.save()
            return session
        except Exception as e:
            return None

    def get_session_if_valid(self, user, session_id):
        """Get session if it is valid and not expired.

        Args:
            user (User): User model object
            session_id (int): Session row id

        Returns:
            Session or None
        """
        try:
            session = self.select_related('user').get(
                user=user,
                id=session_id,
                is_valid=True
            )
            if session.expire_at < now():
                session.is_valid = False
                session.save()
                return None
            return session
        except Exception as e:
            return None

    def get_last_session(self, user):
        return self.filter(user=user).order_by('-created_at').first()

    def get_user(self, session_id):
        try:
            return self.get(id=session_id).user
        except Exception as e:
            return None
