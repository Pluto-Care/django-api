from django.db import models
from django.utils.timezone import now
from datetime import datetime
from users.models import User


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

    def save_due_forgot_password_form(self, user: User):
        try:
            row = self.get(user=user)
            row.date_last_changed_by_user=now()
            row.last_pswd_change_method_by_user='forgot_password'
            row.pswd_change_lock_til=now()+datetime.timedelta(days=1)
            row.save()
        except self.DoesNotExist:
            self.create(
                user=user,
                date_last_changed_by_user=now(),
                last_pswd_change_method_by_user='forgot_password',
                pswd_change_lock_til=now()+datetime.timedelta(days=1)
            )

