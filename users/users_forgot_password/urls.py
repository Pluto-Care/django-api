from django.urls import path
from . import views

"""
/api/user/forgot_password/
"""
urlpatterns = [
    path('request/', views.forgot_password),
    path('validate/', views.check_health),
    path('reset/', views.reset_password),
]
