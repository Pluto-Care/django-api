from django.urls import path, include
from . import views

"""
api/role/
"""
urlpatterns = [
    path('update_permissions/', views.update_permissions),
]
