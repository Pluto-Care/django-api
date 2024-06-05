from django.urls import path, include
from . import views

"""
api/organization/
"""
urlpatterns = [
    path('me/', views.me),
    path('update/', views.createOrUpdateOrgProfile)
]
