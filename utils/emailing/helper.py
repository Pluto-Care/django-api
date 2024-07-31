from django.core.mail import send_mail
from core.settings import getEmailConnection
from decouple import config


def email_send_helper(email_to: str, subject: str, template: str) -> int:
    """ Sends email to the given email address with the given subject and template

    Args:
        email_to (str): Address to send the email to
        subject (str): Subject of the email
        template (str): HTML template to send (See utils/emailing/base_template.py)

    Returns:
        int: 1 = Success, 0 = Failure
    """
    # Send this token
    try:
        with getEmailConnection() as connection:
            html_message = template
            from_email = config('SMTP_DEFAULT_SEND_FROM')
            return send_mail(subject=subject,
                             html_message=html_message,
                             from_email=from_email,
                             recipient_list=[email_to,],
                             connection=connection)
    except Exception as e:
        return 0
