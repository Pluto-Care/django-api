from django.urls import path, include
from . import views

"""
api/phone_call/
"""
urlpatterns = [
    path('token/', views.grant_twilio_token),
    path('twiml/', views.twiml),
    path('register_call_status/', views.register_call_status),
]
