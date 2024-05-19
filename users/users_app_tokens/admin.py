from django.contrib import admin
from .models import AppToken

# Register your models here.


class AppTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_valid', 'ip', 'created_at')
    search_fields = ['user__email', 'user__first_name',
                     'user__last_name', 'id', 'ip']
    search_help_text = 'Search with user\'s first and last name, email, session Id, or IP address.'
    list_per_page = 100
    ordering = ('-created_at',)
    save_on_top = False
    save_as = False
    readonly_fields = ['id', 'user', 'token', 'ip', 'ua', 'created_at']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(AppToken, AppTokenAdmin)
