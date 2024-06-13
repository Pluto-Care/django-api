from django.urls import path, include
from . import views

"""
api/appointment/
"""
urlpatterns = [
    path('new/', views.create_appointment),
    path('list/', views.list_appointments),
    path('id/<str:appointment_id>/', views.AdminAppointmentView.as_view()),
    path('my/', views.my_appointments),
    path('my/<str:appointment_id>/', views.MyAppointmentView.as_view())
]
