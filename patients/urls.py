from django.urls import path, include
from . import views

"""
api/patient/
"""
urlpatterns = [
    path('new/', views.createPatient),
    path('list/', views.listPatients),
    # path('update/', views.updatePatient),
    # path('delete/', views.deletePatient),
    # path('search/', views.searchPatient),
    # path('get/', views.getPatient),
]
