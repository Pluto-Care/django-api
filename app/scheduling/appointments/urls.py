from django.urls import path, include
from . import views

"""
api/scheduling/appointments/
"""
urlpatterns = [
    path('admin/new/', views.create_appointment),
    path('admin/list/', views.list_appointments),
    path('admin/list/<str:appointment_id>/',
         views.AdminAppointmentView.as_view()),

    # My appointments
    path('my/new/', views.create_my_appointment),
    path('my/list/', views.my_appointments),
    path('my/patients/', views.my_appointment_patient_list),

    # date: '06-13-2024' (format: MM-DD-YYYY)
    path('my/date/<str:date>/', views.my_appointments_for_date),

    path('my/list/<str:appointment_id>/', views.MyAppointmentView.as_view()),
    path('my/list/<str:appointment_id>/patient/', views.get_appointment_patient),
]
