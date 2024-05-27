import re
from getpass import getpass
from organizations.api import new_organization
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate encryption keys for project.'

    def handle(self, *args, **kwargs):
        # User TOTP key
        self.stdout.write(
            "\nTo create an organization, enter user details who will admin it.")
        email = input("\nEnter user email: ")
        while not validate_email(email):
            self.stdout.write("[Error] Invalid email.")
            email = input("Enter user email: ")
        password = getpass("Enter user password: ")
        while not validate_password(password):
            self.stdout.write(
                "[Error] Password must be at least 8 characters long and contain at least one digit, one uppercase alphabet, one lowercase alphabet, and one special character.")
            password = getpass("Enter user password: ")
        confirm_password = getpass("Confirm user password: ")
        while password != confirm_password:
            self.stdout.write("[Error] Passwords do not match.")
            password = getpass("Enter user password : ")
            while not validate_password(password):
                self.stdout.write(
                    "[Error] Password must be at least 8 characters long and contain at least one digit, one uppercase alphabet, one lowercase alphabet, and one special character.")
                password = getpass("Enter user password: ")
            confirm_password = getpass("Confirm user password: ")
        first_name = input("Enter user first name: ")
        last_name = input("Enter user last name: ")
        try:
            org = new_organization(email, password, first_name, last_name)
        except Exception as e:
            self.stdout.write(
                f"\nFailed to create organization. Error: {e}")
            return
        if org:
            self.stdout.write(
                "\nOrganization created successfully.")
            self.stdout.write(
                "\nUser created successfully.")
            self.stdout.write(
                f"Organization ID: {org.id}")
        else:
            self.stdout.write(
                "\nFailed to create organization. Please try again.")


def validate_email(value):
    # Check if email is valid
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(regex, value):
        return False
    return True


def validate_password(value):
    # Check if password is at least 8 characters long and contains at least one digit, one uppercase letter, one lowercase letter, and one special character
    regex = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[~#?!@$`\'":;.,%^&*-_+=<>|\/\{\}\[\]\(\)]).{8,}$'
    if not re.match(regex, value):
        return False
    return True
