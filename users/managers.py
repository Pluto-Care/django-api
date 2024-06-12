from django.db import models


class UserManager(models.Manager):
    def __init__(self):
        super().__init__()

    def create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user
