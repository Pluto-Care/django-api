from django.db import models
from django.utils.timezone import now
from datetime import datetime, timedelta


class UserManager(models.Manager):
    def __init__(self):
        super().__init__()

    def create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user


class UserPasswordChangeManager(models.Manager):
    def __init__(self):
        super().__init__()

    def save_due_forgot_password_form(self, user):
        """Create or update a row in the UserPasswordChange table for the user who forgot their password.

        Args:
            user (User): User object
        """
        try:
            row = self.get(user=user)
            row.date_last_changed_by_user = now()
            row.last_pswd_change_method_by_user = 'forgot_password'
            row.pswd_change_lock_til = now()+timedelta(days=1)
            row.save()
        except self.model.DoesNotExist:
            self.create(
                user=user,
                date_last_changed_by_user=now(),
                last_pswd_change_method_by_user='forgot_password',
                pswd_change_lock_til=now()+timedelta(days=1)
            )

    def save_due_change_by_admin(self, user, admin):
        """Create or update a row in the UserPasswordChange table for the user whose password was changed by an admin.

        Args:
            user (User): User object
        """
        try:
            row = self.get(user=user)
            row.date_last_changed_by_admin = now()
            row.last_changed_by_admin = admin
            row.save()
        except self.model.DoesNotExist:
            self.create(
                user=user,
                date_last_changed_by_admin=now(),
                last_changed_by_admin=admin
            )
