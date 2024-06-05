import jwt
from core.settings import SECRET_KEY
from decouple import config
from .models import Session
from .utils import getClientIP, getUserAgent
# Roles Imports
from roles.api import get_user_permissions, get_user_role


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.COOKIE_NAME = config('AUTH_COOKIE_NAME', default='auth')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        session = self.get_active_session(request)
        # Attach the session to the request
        request.active_session = session
        if session:
            request.active_user_role = get_user_role(session.user)
            request.active_user_permissions = get_user_permissions(
                session.user)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_active_session(self, request):
        session = None
        # Check if auth token is present in cookies
        try:
            key = request.COOKIES.get(self.COOKIE_NAME)
            try:
                decoded_jwt_key = jwt.decode(
                    key, SECRET_KEY, algorithms=['HS256'])
            except jwt.InvalidSignatureError:
                return None
            key = decoded_jwt_key.get('session_key')
            session = Session.objects.authenticate_session(
                key, getClientIP(request), getUserAgent(request))
            return session
        except (KeyError, Exception) as e:
            session = None
        return session
