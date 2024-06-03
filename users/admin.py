from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ['first_name', 'last_name',
                     'email']
    search_help_text = 'Search with first name, last name, or email address.'
    sortable_by = ['first_name', 'last_name', 'email']
    list_per_page = 50
    ordering = ('-created_at',)
    save_on_top = False
    save_as = False
    readonly_fields = ['created_at', 'password']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(User, UserAdmin)
