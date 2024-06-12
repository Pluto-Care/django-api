from django.urls import path, include
from . import views

"""
api/appointment/
"""
urlpatterns = [
    path('new/', views.create_appointment),
    path('list/', views.list_appointments),
    path('id/<str:appointment_id>/', views.AppointmentView.as_view())
]
