from rest_framework import serializers
from .models import Patient
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


# Serializers

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'dob', 'street', 'city',
                  'state', 'postal_code', 'country', 'phone', 'email',
                  'created_at', 'updated_at', 'created_by', 'updated_by', 'organization']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
            'organization': {'required': True, 'read_only': True},
            'email': {'validators': [validate_email]},
            'first_name': {'required': True},
            'last_name': {'required': True}}
