import json
from .models import ApiCallLog
from .log_response import LogResponse


class APILogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        # Don't run on non-API requests
        if not request.path.startswith('/api'):
            return response
        # Create log
        try:
            content = json.loads(response.content.decode('utf8'))
        except json.JSONDecodeError:
            # If response is not JSON or empty
            content = dict()
        if response.status_code > 399:
            if 'instance' in content:
                # Omit instance as it is from ErrorMessage class
                # instance also carries the URL that caused the error
                # but this information is already in model's URL column
                content.pop('instance')
            if 'status' in content:
                # Omit status as it is already in model's status column
                content.pop('status')
            log = LogResponse(status=response.status_code, message=content)
        else:
            # check if content has key 'session_id', that means this
            # response is from login or signup API
            if 'user' in content:
                log = LogResponse(status=response.status_code, message=dict(
                    user=content['user']['email']))
            else:
                log = LogResponse(status=response.status_code)
        ApiCallLog.objects.create_log(
            request=request,
            response=log.serialize(),
        )
        return response
