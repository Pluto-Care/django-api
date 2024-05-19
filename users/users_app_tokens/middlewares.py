from .models import AppToken
from django.utils.encoding import force_str
from .utils import getUserAgent


class AppTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # This gets executed before the view.
        # Get the active session
        app_token = self.get_active_app_token(request)
        # Attach the session to the request
        request.active_token = app_token

    def get_active_app_token(self, request):
        apptoken = None
        # Check if auth token is present in header
        if apptoken is None and 'Authorization' in request.headers:
            token = force_str(request.headers['Authorization'])
            if token is None:
                return None
            token = token.split(' ')[-1]  # Get the token from 'Bearer <token>'
            return AppToken.objects.authenticate_app_token(token, getUserAgent(request))
        return apptoken
