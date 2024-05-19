import json
from django.contrib import admin
from .models import ApiCallLog
from users.users_app_tokens.api import get_user as get_user_from_app_token
from users.users_sessions.api import get_user as get_user_from_session

# Register your models here.


class ApiCallLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'url', 'status', 'ip', 'created_at')
    search_fields = ['id', 'session', 'app_token', 'url', 'ip']
    search_help_text = 'Search with Id, URL and session id, token id, or IP address.'
    list_per_page = 50
    ordering = ('-created_at',)
    save_on_top = False
    save_as = False
    readonly_fields = ['url', 'context', 'session', 'ip', 'ua',
                       'app_token', 'status', 'created_at']

    def user_email(self, obj):
        if obj.app_token:
            user = get_user_from_app_token(obj.app_token)
            if user:
                return user.email
        elif obj.session:
            user = get_user_from_session(obj.session)
            if user:
                return user.email
        else:
            context = json.loads(obj.context)
            if 'm' in context and 'user' in context['m']:
                """This only works for login and sign up requests as the APILogMiddleware
                the user object and store it in log context"""
                return context['m']['user']
        return '---'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(ApiCallLog, ApiCallLogAdmin)
