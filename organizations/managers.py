from django.db import models


class OrganizationManager(models.Manager):
    def __init__(self):
        super().__init__()

    def create_org(self):
        row = self.create()
        return row


class OrgUserManager(models.Manager):
    def __init__(self):
        super().__init__()

    def create_org_user(self, organization, user):
        row = self.create(
            organization=organization,
            user=user
        )
        return row


class OrgProfileManager(models.Manager):
    def __init__(self):
        super().__init__()
