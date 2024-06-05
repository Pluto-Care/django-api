from django.contrib import admin
from .models import Organization, OrgUser, OrgProfile

admin.site.register(OrgProfile)
admin.site.register(OrgUser)
admin.site.register(Organization)
