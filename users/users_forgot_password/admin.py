from django.contrib import admin
from .models import ForgotPassword

# Register your models here.


class ForgotPasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_valid', 'is_used', 'ip', 'created_at')
    search_fields = ['user__email', 'user__first_name',
                     'user__last_name', 'id', 'ip']
    search_help_text = 'Search with user\'s first and last name, email, session id, or IP address.'
    list_per_page = 100
    ordering = ('-created_at',)
    save_on_top = False
    save_as = False
    readonly_fields = ['id', 'user', 'key', 'ip', 'ua',
                       'created_at', 'updated_at', 'is_used']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(ForgotPassword, ForgotPasswordAdmin)
