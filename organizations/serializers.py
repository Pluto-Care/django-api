from rest_framework import serializers
from .models import OrgProfile
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

class OrgProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgProfile
        fields = ['city', 'country', 'created_at', 'email', 'name', 'organization',
                  'phone', 'postal_code', 'state', 'street', 'updated_at', 'updated_by']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'email': {'required': True, 'validators': [validate_email]}
        }
