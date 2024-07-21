from django.urls import path, include
from . import views
from . import views_user

"""
api/organization/
"""
urlpatterns = [
    path('me/', views.OrgProfileView.as_view()),

    # Manage users
    path('manage/user/create/', views_user.create_org_user),
    path('manage/users/', views.get_org_users),
    path('manage/users/search/', views.search_org_users),
    path('manage/users/<str:user_id>/', views_user.OrgUserView.as_view()),
    path('manage/users/<str:user_id>/reset_password/',
         views_user.reset_org_user_password),
    path('manage/users/<str:user_id>/update_profile/',
         views.update_org_user_profile),
]
