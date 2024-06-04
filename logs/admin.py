from django.contrib import admin
from .models import ApiCallLog
from django.db.models import Q

# Register your models here.


class IsAuthFilter(admin.SimpleListFilter):
    title = 'Authenticated'
    parameter_name = 'is_auth'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(Q(session=None) & Q(app_token=None))
        elif self.value() == 'no':
            return queryset.filter(Q(session=None) & Q(app_token=None))


class IsSuccessFilter(admin.SimpleListFilter):
    title = 'Success'
    parameter_name = 'is_success'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(status__gte=200, status__lt=300)
        elif self.value() == 'no':
            return queryset.exclude(status__gte=200, status__lt=300)


class SessionTypeFilter(admin.SimpleListFilter):
    title = 'Session Type'
    parameter_name = 'session_type'

    def lookups(self, request, model_admin):
        return (
            ('session', 'Session (Web)'),
            ('app_token', 'App Token (Mobile)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'session':
            return queryset.exclude(session=None)
        elif self.value() == 'app_token':
            return queryset.exclude(app_token=None)


class ApiCallLogAdmin(admin.ModelAdmin):
    list_display = ('url', 'user_email', 'status', 'ip', 'created_at')
    search_fields = ['id', 'session', 'app_token', 'url', 'ip']
    list_filter = (IsAuthFilter, IsSuccessFilter,
                   SessionTypeFilter, 'created_at')
    search_help_text = 'Search with id, URL and session id, token id, or IP address.'
    list_per_page = 50
    ordering = ('-created_at',)
    save_on_top = False
    save_as = False
    readonly_fields = ['id', 'url', 'context', 'session', 'ip', 'ua',
                       'app_token', 'status', 'created_at']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(ApiCallLog, ApiCallLogAdmin)
