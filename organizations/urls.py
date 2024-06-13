from django.urls import path, include
from . import views

"""
api/organization/
"""
urlpatterns = [
    path('me/', views.OrgProfileView.as_view()),
    path('user/create/', views.create_org_user),
    path('users/', views.get_org_users),
    path('users/search/', views.search_org_users),
    path('users/<str:user_id>/', views.OrgUserView.as_view()),
]
