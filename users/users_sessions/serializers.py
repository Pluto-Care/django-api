from .models import Session
from rest_framework import serializers


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'key', 'user', 'expire_at',
                  'is_valid', 'created_at', 'updated_at', 'ip', 'ua']
        extra_kwargs = {
            'key': {'required': True, 'write_only': True},
            'user': {'required': True},
        }


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'is_valid', 'created_at', 'updated_at', 'ip', 'ua']
