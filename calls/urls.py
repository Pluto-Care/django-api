from django.urls import path, include
from . import views

"""
api/phone_call/
"""
urlpatterns = [
    path('make/', views.make_call),
]
