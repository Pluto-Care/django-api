import os
import string
import random
from core.settings import PROJECT_BASE_DIR


KEY_PATH = os.path.join(PROJECT_BASE_DIR, 'keys',
                        'users_totp_key.bin')


def generate_backup_codes():
    """Generate backup codes for the user

    Returns:
        list: A list of backup codes
    """
    backup_codes = []
    for _ in range(6):
        backup_code = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=8))
        backup_codes.append(backup_code)
    return backup_codes
