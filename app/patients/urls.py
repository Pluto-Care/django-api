from django.urls import path, include
from . import views

"""
api/patients/
"""
urlpatterns = [
    path('new/', views.createPatient),
    path('list/', views.listPatients),
    path('list/<str:patient_id>/', views.PatientView.as_view()),
    path('list/<str:patient_id>/notes/', views.get_patient_notes),
    path('list/<str:patient_id>/notes/new/', views.create_patient_note),
    path('list/<str:patient_id>/notes/<str:note_id>/',
         views.PatientNoteView.as_view()),
    path('search/', views.search_patient),
]
