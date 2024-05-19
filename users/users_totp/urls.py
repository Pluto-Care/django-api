from django.urls import path
from . import views

"""
api/user/totp/
"""
urlpatterns = [
    path('init/', views.totp_init),
    path('enable/', views.totp_enable),
    path('disable/', views.totp_disable),
    path('new-backup-codes/', views.totp_new_backup_codes),
]
