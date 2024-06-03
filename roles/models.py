from django.db import models
from django.utils.timezone import now
from users.models import User


class Permission(models.Model):
    # create, read, update, delete, disable, enable etc. e.g. update:user_password
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)


class Role(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, default=None)


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)


# User Permission take precedence over Role Permission
class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
