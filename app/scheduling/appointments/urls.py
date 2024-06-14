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
    path('my/list/<str:appointment_id>/', views.MyAppointmentView.as_view())
]
