from django.contrib import admin
from .models import Totp

# Register your models here.


class TotpAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'status', 'created_at')
    search_fields = ['user__email']
    search_help_text = 'Search with user email.'
    list_per_page = 100
    ordering = ('-created_at',)
    save_on_top = False
    save_as = False
    readonly_fields = ['user', 'key', 'backup_codes', 'bc_attempts', 'bc_timeout',
                       'created_at', 'updated_at']

    def active(self, obj):
        return obj.status == 'enabled'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Totp, TotpAdmin)
