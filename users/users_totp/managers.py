import pyotp
from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from .utils import generate_backup_codes, KEY_PATH
from security.encryption import encrypt, decrypt
from django.db.models import Q


class TotpManager(models.Manager):
    def __init__(self):
        super().__init__()
        # Timeout when incorrect backup codes are
        # entered more than 3 times
        self.BC_ATTEMPTS = 3
        self.BC_TIMEOUT = timedelta(minutes=30)

    def create_totp(self, user):
        # Get the user's totp objects. It should ideally be only one.
        # If status is enabled or backup_used, then user already has totp enabled
        # We do not want to create a new totp object
        totp_row = self.filter(Q(user=user), ~Q(status='disabled'))
        for row in totp_row:
            if row.status == 'enabled' or row.status == 'backup_used':
                return None
            # If status is initialized, then we delete the old totp object
            # This is to prevent multiple totp objects for the same user
            if row.status == 'initialized':
                row.delete()
        # Create a new totp object
        key = pyotp.random_base32()
        backup_codes = generate_backup_codes()
        totp = self.create(
            user=user,
            key=encrypt(KEY_PATH, key),
            backup_codes=encrypt(KEY_PATH, backup_codes)
        )
        return key, backup_codes, totp

    def get_totp(self, user):
        try:
            return self.get(Q(user=user), ~Q(status='disabled'))
        except Exception as e:
            return None

    def authenticate(self, user, token, totp_row=None):
        """Authenticate the user using the 6 or 8 length token.

        Exception:
            Throws an exception if the user does not have TOTP enabled/initialized/backup_used.

        Args:
            user (User): Model object
            token (str): 6 len OTP or 8 len backup code
            totp_row (Totp) (optional): Only provide if you are sure that the totp
                             belongs to the same user.
                             Otherwise, it is recommended to not provide this argument.

        Returns:
            Totp or None: Returns Totp when authenticated, None otherwise
        """
        # Check based on the length of the token
        if len(token) == 6:
            # OTP is being used
            if totp_row is None:
                totp_row = self.get_totp(user)  # Get the totp object
                if totp_row is None:
                    return None
            # Get the key from the totp object
            key = decrypt(KEY_PATH, totp_row.key)
            # Verify the token using the key
            if pyotp.TOTP(key).verify(token):
                # Clear out any backup code attempts
                if totp_row.bc_attempts > 0:
                    totp_row.bc_attempts = 0
                    totp_row.bc_timeout = None
                    totp_row.save()
                # Return the totp object
                # The OTP is authenticated
                return totp_row
        elif len(token) == 8:
            # Backup code is being used
            if totp_row is None:
                totp_row = self.get_totp(user)
                if totp_row is None:
                    return None
            # Check if backup code attempts are timed out
            if totp_row.bc_timeout is not None and now() < totp_row.bc_timeout:
                # Here we assume that the user user is compromised
                # therefore, we simply return None indicating TOTP failure.
                # We also assume that the actual user will use the OTP to login
                # and the possibility for user to use the backup code at the same
                # time is very low.
                return None
            # Only accept backup token if the status is enabled or backup_used
            if totp_row.status == 'enabled' or totp_row.status == 'backup_used':
                # Check if the token is a backup code
                backup_codes = decrypt(KEY_PATH, totp_row.backup_codes)
                if token in backup_codes:
                    backup_codes.remove(token)
                    totp_row.backup_codes = encrypt(KEY_PATH, backup_codes)
                    totp_row.status = 'backup_used'
                    totp_row.bc_attempts = 0
                    totp_row.bc_timeout = None
                    totp_row.updated_at = now()
                    totp_row.save()
                    return totp_row
                else:
                    # Increment the backup code attempts
                    # If more than 3, then set the timeout
                    totp_row.bc_attempts += 1
                    if totp_row.bc_attempts > self.BC_ATTEMPTS:
                        totp_row.bc_attempts = 0  # Refresh attempts as timeout is issued
                        totp_row.bc_timeout = now() + self.BC_TIMEOUT
                    totp_row.save()
                    return None
        else:
            return None

    def disable_totp(self, user):
        try:
            self.get(Q(user=user), ~Q(status='disabled')
                     ).update(status='disabled')
        except Exception as e:
            pass

    def create_new_backup_codes(self, user):
        """Create new backup codes for the user. Invalidates old backup codes.

        Args:
            user (User)

        Returns:
            list[str] or None: New backup codes
        """
        try:
            backup_codes = generate_backup_codes()
            # Get the user's totp object
            totp_row = self.get(Q(user=user), ~Q(status='disabled'))
            # Update the backup codes
            totp_row.backup_codes = encrypt(KEY_PATH, backup_codes)
            totp_row.status = 'enabled'
            totp_row.updated_at = now()
            totp_row.save()
            # Return the new backup codes
            return backup_codes
        except Exception as e:
            return None
