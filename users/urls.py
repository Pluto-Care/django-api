from django.urls import path, include
from . import views

"""
api/user/
"""
urlpatterns = [
    path('create/', views.signup),
    path('login/', views.login),
    path('token_login/', views.token_login),
    path('logout/', views.logout),
    path('totp/', include('users.users_totp.urls')),
    path('forgot_password/',
         include('users.users_forgot_password.urls')),
]
