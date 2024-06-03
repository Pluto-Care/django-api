from users.api import get_request_user
from .models import UserRole, UserPermission


class AttachPermissionsMiddleware:
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
        user = get_request_user(request)
        if user:
            user_permissions = UserPermission.objects.filter(user=user)
            user_role = UserRole.objects.select_related(
                'role').filter(user=user).first()
            if user_role:
                user_permissions = user_permissions.union(
                    user_role.role.permissions.all()).values_list('id', flat=True)
            else:
                user_permissions = user_permissions.values_list(
                    'permission__id', flat=True)
            request.active_permissions = list(user_permissions)
