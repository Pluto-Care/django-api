from django.urls import path, include
from . import views

"""
api/patient/
"""
urlpatterns = [
    path('new/', views.createPatient),
    path('list/', views.listPatients),
    path('search/', views.search_patient),
    path('id/<str:patient_id>/', views.PatientView.as_view()),
    # path('search/', views.searchPatient),
]
