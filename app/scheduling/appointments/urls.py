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
    path('my/list/', views.my_appointments),

    # date: '06-13-2024' (format: MM-DD-YYYY)
    path('my/list/<str:date>/', views.my_appointments_for_date),

    path('my/list/<str:appointment_id>/', views.MyAppointmentView.as_view())
]
