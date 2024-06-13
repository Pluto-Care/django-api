from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'start_at', 'end_at', 'reason', 'status', 'assigned_to',
                  'created_at', 'updated_at', 'created_by', 'updated_by', 'organization']
        extra_kwargs = {
            'organization': {'required': True},
            'patient': {'required': True},
            'start_at': {'required': True},
            'end_at': {'required': True},
            'reason': {'required': True},
            'status': {'required': True}}
