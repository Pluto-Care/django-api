from .templates.new_user_account import new_user_account_template
from .templates.forgot_password import forgot_password_template
from .templates.reset_password_success import reset_password_success_template
from core.settings import getEmailConnection
from django.core.mail import send_mail
from decouple import config


def send_welcome_email(first_name: str, verification_url: str, email: str, subject='Welcome to Pluto Health'):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `verification_key` (str): Verification token
        `email` (str): Recipient email address.
        `subject` (str, optional): Email subject. Defaults to 'Welcome to Pluto Health'.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = new_user_account_template(first_name, verification_url, subject)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {first_name},\n\nPlease verify your email by clicking the link below.\n\n{verification_url}"
            return send_mail(subject=subject,
                             message=message,
                             html_message=template,
                             from_email=config('SMTP_DEFAULT_SEND_FROM'),
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0


def send_forgot_password_email(first_name: str, reset_url: str, email: str, ip: str, subject='Reset your password'):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `verification_key` (str): Verification token
        `email` (str): Recipient email address.
        `ip` (str): IP address of the user requesting password reset.
        `subject` (str, optional): Email subject. Defaults to 'Welcome to Pluto Health'.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = forgot_password_template(first_name, reset_url, ip, subject)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {first_name},\n\nPlease reset your password by clicking the link below.\n\n{reset_url}"
            return send_mail(subject=subject,
                             message=message,
                             html_message=template,
                             from_email=config('SMTP_DEFAULT_SEND_FROM'),
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0


def send_password_changed_email(first_name: str, email: str, subject='Password was changed'):
    """Send a welcome email to a new user

    Args:
        `first_name` (str): Users first name
        `subject` (str, optional): Email subject. Defaults to 'Welcome to Pluto Health'.

    Returns:
        `int`: Returns 0 if fails.
    """
    template = reset_password_success_template(first_name, subject)
    try:
        with getEmailConnection() as connection:
            message = f"Hello {first_name},\n\nYour password was successfully changed. If you did not make this change, please contact our support immediately."
            return send_mail(subject=subject,
                             message=message,
                             html_message=template,
                             from_email=config('SMTP_DEFAULT_SEND_FROM'),
                             recipient_list=[email,],
                             connection=connection)
    except Exception as e:
        return 0
