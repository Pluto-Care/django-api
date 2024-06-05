import jwt
from core.settings import SECRET_KEY
from .models import AppToken
from django.utils.encoding import force_str
from .utils import getUserAgent
# Roles Imports
from roles.api import get_user_permissions, get_user_role


class AppTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        app_token = self.get_active_app_token(request)
        # Attach the session to the request
        request.active_token = app_token
        if app_token:
            request.active_user_role = get_user_role(app_token.user)
            request.active_user_permissions = get_user_permissions(
                app_token.user)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_active_app_token(self, request):
        apptoken = None
        # Check if auth token is present in header
        if apptoken is None and 'Authorization' in request.headers:
            token = force_str(request.headers['Authorization'])
            if token is None:
                return None
            token = token.split(' ')[-1]  # Get the token from 'Bearer <token>'
            try:
                decoded_jwt_token = jwt.decode(
                    token, SECRET_KEY, algorithms=['HS256'])
                token = decoded_jwt_token.get('app_token')
                return AppToken.objects.authenticate_app_token(token, getUserAgent(request))
            except jwt.InvalidSignatureError:
                apptoken = None
        return apptoken
