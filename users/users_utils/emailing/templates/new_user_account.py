from utils.emailing.base_template import base_template


def new_user_account_template(first_name, url, email_subject='Welcome to Pluto Health'):
    return base_template(
        subject=email_subject,
        headline="Let's get you upto speed!",
        message=[
            'Hi ' + first_name + ',',
            'We are excited to have you onboard.',
            'Use the button below to activate your account.',
        ],
        button_text='Activate Account',
        button_link=url,
    )
