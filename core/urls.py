from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls')),
    path('api/organization/', include('organizations.urls')),
    path('api/role/', include('roles.urls')),
    path('api/phone_call/', include('app.calls.urls')),
    path('api/patient/', include('app.patients.urls')),
    path('api/appointment/', include('app.appointments.urls')),
]
