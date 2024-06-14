from rest_framework import serializers
from django.utils.timezone import now
from .models import Appointment, Cancellation


# Validate start time is greater than current time
def validate_start_time(value):
    if value <= now():
        raise serializers.ValidationError(
            "Start time must be greater than current time.")


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'start_time', 'end_time', 'end_time_expected', 'type',
                  'reason', 'status', 'assigned_to', 'logs',
                  'created_at', 'updated_at', 'created_by', 'updated_by', 'organization']
        extra_kwargs = {
            'organization': {'required': True},
            'patient': {'required': True},
            'start_time': {'required': True, 'validators': [validate_start_time]},
            'end_time_expected': {'required': True},
            'type': {'required': True},
            'reason': {'required': True},
            'status': {'required': True}}

    def validate(self, attrs):
        if attrs['end_time_expected'] <= attrs['start_time']:
            raise serializers.ValidationError(
                "End date must be greater than start date.")
        return super().validate(attrs)


class CancellationSerializer(serializers.Serializer):
    class Meta:
        model = Cancellation
        fields = ['id', 'appointment', 'reason',
                  'cancelled_at', 'cancelled_by']
        extra_kwargs = {
            'appointment': {'required': True},
            'reason': {'required': True},
            'cancelled_by': {'required': True}}
