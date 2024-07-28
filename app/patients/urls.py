from django.urls import path, include
from . import views

"""
api/patients/
"""
urlpatterns = [
    path('new/', views.createPatient),
    path('list/', views.listPatients),
    path('list/<str:patient_id>/', views.PatientView.as_view()),
    path('search/', views.search_patient),
    path('list/<str:patient_id>/notes/',
         include('app.patients.patients_notes.urls')),
]
