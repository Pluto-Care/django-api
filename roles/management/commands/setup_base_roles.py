from django.core.management.base import BaseCommand
from roles.models import Permission, Role
from roles.base_permissions import base_permission, base_roles
from app.patients.base_permissions import base_permission as patients_base_permission
from app.calls.base_permissions import base_permission as calls_base_permission
from app.scheduling.base_permissions import base_permission as scheduling_base_permission


class Command(BaseCommand):
    help = 'Generate base permission and roles.'

    def handle(self, *args, **kwargs):
        permissions = dict()
        # --------------------------------------#
        # Create permissions
        # Roles App
        for key, value in base_permission.items():
            permission = Permission(id=value['id'], name=value['name'])
            permission.save()
            permissions[value['id']] = permission
        # Patients App
        for key, value in patients_base_permission.items():
            permission = Permission(id=value['id'], name=value['name'])
            permission.save()
            permissions[value['id']] = permission
        # Calls App
        for key, value in calls_base_permission.items():
            permission = Permission(id=value['id'], name=value['name'])
            permission.save()
            permissions[value['id']] = permission
        # Scheduling App
        for key, value in scheduling_base_permission.items():
            permission = Permission(id=value['id'], name=value['name'])
            permission.save()
            permissions[value['id']] = permission
        # --------------------------------------#
        # Create roles
        for role in base_roles:
            role_name = role['name']
            role_permissions = []
            for permission in role['permissions']:
                if permission['id'] in permissions:
                    role_permissions.append(permissions[permission['id']])
            role = Role(name=role_name)
            role.save()
            role.permissions.set(role_permissions)
            role.save()
        self.stdout.write(self.style.SUCCESS(
            'Successfully created base permissions and roles.'))
