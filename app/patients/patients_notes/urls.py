from django.urls import path, include
from . import views

"""
api/patients/list/<str:patient_id>/notes/
"""
urlpatterns = [
    path('general/', views.get_general_notes),
    path('general/new/', views.create_general_note),
    path('general/<str:note_id>/',
         views.GeneralNoteView.as_view()),
    path('doctor/', views.get_doctor_notes),
    path('doctor/new/', views.create_doctor_note),
    path('doctor/<str:note_id>/',
         views.DoctorNoteView.as_view()),
]
