from django.utils.encoding import force_str
from rest_framework import serializers
from .models import User
from .api import get_user
import re

# Validators


def validate_email(value):
    # Check if email is valid
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(regex, value):
        raise serializers.ValidationError('Email is not valid.')
    # Lowercase email
    value = value.lower()
    return value


def validate_password(value):
    # Check if password is at least 8 characters long and contains at least one digit, one uppercase letter, one lowercase letter, and one special character
    regex = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[~#?!@$`\'":;.,%^&*-_+=<>|\/\{\}\[\]\(\)]).{8,}$'
    if not re.match(regex, value):
        raise serializers.ValidationError(
            'Password must be at least 8 characters long and contain at least one digit, one uppercase alphabet, one lowercase alphabet, and one special character.')
    return value


# Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_admin', 'is_active', 'created_at', 'first_name', 'last_name',
                  'updated_at', 'email', 'password', 'created_by', 'updated_by']
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'validators': [validate_password]},
                        'created_at': {'read_only': True},
                        'email': {'required': True, 'validators': [validate_email]},
                        'first_name': {'required': True},
                        'id': {'required': False},
                        'last_name': {'required': True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # Check if email and password are provided
        if 'email' not in data or 'password' not in data:
            raise serializers.ValidationError(
                'All fields are required.')
        user = get_user(force_str(data['email']))
        if user:
            # Check if password is correct
            if not user.check_password(force_str(data['password'])):
                raise serializers.ValidationError('Credentials are invalid.')
            # Check if user is active
            if not user.is_active:
                raise serializers.ValidationError('Account is disabled.')
        else:
            raise serializers.ValidationError('Credentials are invalid.')
        return user


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate(self, data):
        # Check if password is provided
        if 'password' not in data:
            raise serializers.ValidationError('Password is required.')
        # validate password
        return validate_password(force_str(data['password']))
