from Crypto.Random import get_random_bytes
from users.users_totp.utils import KEY_PATH


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate encryption keys for project.'

    def handle(self, *args, **kwargs):
        # User TOTP key
        with open(KEY_PATH, 'wb') as f:
            f.write(get_random_bytes(32))
        self.stdout.write("Key generated successfully.")
