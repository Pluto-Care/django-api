from .models import AppToken
from rest_framework import serializers


class AppTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppToken
        fields = ['id', 'token', 'user', 'is_valid', 'created_at', 'ip', 'ua']
        extra_kwargs = {
            'token': {'required': True, 'write_only': True},
            'user': {'required': True},
        }


class UserAppTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppToken
        fields = ['id', 'is_valid', 'created_at', 'ip', 'ua']
