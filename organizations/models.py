from django.db import models
from django.utils.timezone import now
from users.models import User
from .managers import OrganizationManager, OrgUserManager


class Organization(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
    created_at = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)

    objects = OrganizationManager()


class OrgUser(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = OrgUserManager()
