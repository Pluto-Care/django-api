from rest_framework.views import exception_handler
from .error_message import ErrorMessage
import json


def drf_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        error = ErrorMessage(
            title=response.data['detail'],
            detail=response.data['detail'],
            status=response.status_code,
            instance=context['request'].build_absolute_uri(),
            code='DRF001'
        )
        response.data = json.dumps(error.serialize())
        response.content = json.dumps(error.serialize())
        response['Content-Type'] = 'application/problem+json'

    return response
