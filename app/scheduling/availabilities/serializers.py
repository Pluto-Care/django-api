from rest_framework import serializers
from .models import Availability, Break


# Validator to check if start_time is less than end_time
def validate_time(start_time, end_time):
    if start_time >= end_time:
        raise serializers.ValidationError(
            "End time must be greater than start time.")


# Validator to check if start_date is less than end_date
def validate_date(start_date, end_date):
    if start_date >= end_date:
        raise serializers.ValidationError(
            "End date must be greater than start date.")


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'user', 'start_time', 'end_time', 'start_date',
                  'end_date', 'weekdays', 'recurring', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': True},
            'start_time': {'required': True},
            'end_time': {'required': True, 'validators': [validate_time]},
            'start_date': {'required': True},
            'end_date': {'required': True, 'validators': [validate_date]},
            'weekdays': {'required': True},
            'recurring': {'required': True}
        }


class BreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Break
        fields = ['id', 'availability', 'start_time', 'end_time', 'start_date',
                  'end_date', 'reason', 'created_at', 'updated_at']
        extra_kwargs = {
            'availability': {'required': True},
            'start_time': {'required': True},
            'end_time': {'required': True, 'validators': [validate_time]},
            'start_date': {'required': True},
            'end_date': {'required': True, 'validators': [validate_date]},
            'reason': {'required': True}
        }
