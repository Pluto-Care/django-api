from utils.emailing.base_template import base_template


def reset_password_success_template(first_name, email_subject='Password was changed'):
    return base_template(
        subject=email_subject,
        headline="Password was changed",
        message=[
            'Hi' + first_name + ',',
            'Your password was successfully changed. If you did not make this change, please contact our support immediately.',
            '',
            'https://support.plutohealth.com/'
            '',
            'Thank you for using our services.',
        ]
    )
