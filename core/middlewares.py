import json
from django.http import JsonResponse
from core.settings import ALLOW_ORIGINS, DEBUG
from utils.error_handling.error_message import ErrorMessage


class APIRequestFormatMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Run on API requests only
        if request.path.startswith('/api') and request.content_type == 'application/json':
            if not self.validate_json_payload(request):
                error = ErrorMessage(
                    detail='Invalid JSON payload.',
                    status=400,
                    instance=request.build_absolute_uri(),
                    title='Invalid data provided'
                )
                return JsonResponse(
                    error.serialize(),
                    status=400)

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def validate_json_payload(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                request.data = json.loads(request.body)
                return True
            except json.JSONDecodeError:
                return False
        return True


class RequestOriginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Run on API requests only
        if request.path.startswith('/api'):
            # If Token authentication is used that means
            # the API is accessed by a non-web application.
            # In that case, we don't need to check the origin.
            # OTHERWISE check the origin header!
            if request.active_token is None:
                if not self.validate_origin_header(request):
                    error = ErrorMessage(
                        detail='You are not authorized to perform this action.',
                        status=400,
                        instance=request.build_absolute_uri(),
                        title='Action not allowed.'
                    )
                    return JsonResponse(
                        error.serialize(),
                        status=400)

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def validate_origin_header(self, request):
        # If DEBUG is True, allow all origins
        if DEBUG:
            return True
        # If ALLOW_ORIGINS is set to '*', allow all origins
        if ALLOW_ORIGINS[0] == '*':
            return True
        # Check if the request origin is in ALLOW_ORIGINS
        if request.headers.get('Origin') in ALLOW_ORIGINS:
            return True
        return False


class HeaderRequestedByMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Run on API requests only
        if request.path.startswith('/api'):
            # If 'X-Requested-By' header is present and not set to 'web'
            # then token based authentication is used. In such case,
            # provide 'Authorization' header with token.
            if 'HTTP_X_REQUESTED_BY' in request.META:
                request.requested_by = request.META['HTTP_X_REQUESTED_BY']
            else:
                request.requested_by = 'web'

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response


def is_web(request):
    return request.requested_by == 'web'


class FormulateResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        if request.path.startswith('/api') and "Content-Type" in response.headers and response.headers["Content-Type"] in ['application/json', 'application/problem+json']:
            response_format = dict(
                success=None,
                data=None,
                errors=None,
                status=response.status_code
            )
            if response.status_code > 399 and response.status_code < 500:
                response_format['success'] = False
                response_format['errors'] = json.loads(
                    response.content.decode('utf8'))
            elif response.status_code < 300:
                response_format['success'] = True
                if response.status_code != 204 and response.content:
                    response_format['data'] = json.loads(
                        response.content.decode('utf8'))
                if response.status_code == 204:
                    response.status_code = 200
                    response_format['status'] = 200
            response.content = json.dumps(response_format)
        elif request.path.startswith('/api') and "Content-Type" not in response.headers:
            response_format = dict(
                success=response.status_code < 300,
                data=None,
                errors=None,
                status=200
            )
            response.content = json.dumps(response_format)
            response.status_code = 200
        return response
