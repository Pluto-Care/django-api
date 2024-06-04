from django.contrib import admin
from .models import Role, Permission, UserRole, UserPermission

# Register your models here.


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Role, RoleAdmin)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Permission, PermissionAdmin)


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')


admin.site.register(UserRole, UserRoleAdmin)


class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission', 'created_at')


admin.site.register(UserPermission, UserPermissionAdmin)
