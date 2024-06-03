from django.core.management.base import BaseCommand
from roles.models import Permission, Role
from roles.base import base_permission, base_roles


class Command(BaseCommand):
    help = 'Generate base permission and roles.'

    def handle(self, *args, **kwargs):
        permissions = dict()
        # Create permissions
        for key, value in base_permission.items():
            permission = Permission(id=value['id'], name=value['name'])
            permission.save()
            permissions[value['id']] = permission
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
