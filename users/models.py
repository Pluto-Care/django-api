import uuid
from django.db import models
from django.utils.timezone import now
from .managers import UserManager, UserPasswordChangeManager
import bcrypt


class User(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    password = models.CharField(max_length=150)
    email = models.CharField(
        max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    timezone = models.CharField(max_length=150, default='America/Vancouver')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name='user_created_by', null=True, blank=True)
    updated_at = models.DateTimeField(default=now)
    updated_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name='user_updated_by', null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.email

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.save()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class UserPasswordChange(models.Model):
    method_choices = (
        ('authenticated', 'authenticated'),
        ('forgot_password', 'forgot_password'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pswd_user', null=True, blank=True)
    date_last_changed_by_user = models.DateTimeField(default=None, null=True)
    date_last_changed_by_admin = models.DateTimeField(default=None, null=True)
    last_changed_by_admin = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='pswd_changed_by', null=True, blank=True)
    last_pswd_change_method_by_user = models.CharField(max_length=32, choices=method_choices, default=None, null=True)
    pswd_change_lock_til = models.DateTimeField(default=None, null=True)

    objects = UserPasswordChangeManager()
