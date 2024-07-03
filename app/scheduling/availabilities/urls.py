from django.urls import path, include
from . import views

"""
api/scheduling/availabilities/
"""
urlpatterns = [
    path('new/', views.add_availability),
    path('list/', views.list_all),
    path('list/<str:availability_id>/',
         views.AvailabilityView.as_view()),
]
