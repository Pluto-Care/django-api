from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls')),
    path('api/organization/', include('organizations.urls')),
    path('api/phone_call/', include('calls.urls')),
]
