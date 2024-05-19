from utils.emailing.base_template import base_template


def forgot_password_template(first_name, url, ip, email_subject='Reset your password'):
    return base_template(
        subject=email_subject,
        headline="Forgot your password?",
        message=[
            'Hi' + first_name + ',',
            'We received a request to reset your password. Use the button below to reset your password.',
            '',
            'If you did not request a password reset, please ignore this email.',
            'IP requesting reset: ' + ip,
        ],
        button_text='Reset Password',
        button_link=url,
    )
