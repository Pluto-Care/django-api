from django.urls import path, include
from . import views

"""
api/scheduling/availabilities/
"""
urlpatterns = [
    path('admin/new/', views.add_availability),
    path('admin/<str:user_id>/list/', views.list_all),
    path('admin/<str:user_id>/list/<str:availability_id>/',
         views.AvailabilityView.as_view()),
]
