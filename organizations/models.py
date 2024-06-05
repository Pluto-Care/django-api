from django.db import models
from django.utils.timezone import now
from users.models import User
from .managers import OrganizationManager, OrgUserManager, OrgProfileManager


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


class OrgProfile(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = OrgProfileManager()
