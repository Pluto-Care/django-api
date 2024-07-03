from django.urls import path, include
from . import views

"""
api/scheduling/
"""
urlpatterns = [
    path('appointments/', include('app.scheduling.appointments.urls')),
    path('availabilities/', include('app.scheduling.availabilities.urls')),
    path('breaks/', include('app.scheduling.breaks.urls')),
    path('leaves/', include('app.scheduling.leaves.urls')),
]
