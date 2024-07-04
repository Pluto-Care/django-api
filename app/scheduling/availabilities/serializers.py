from rest_framework import serializers
from .models import Availability


# Validator to check if start_time is less than end_time
def validate_time(self):
    if self.start_time >= self.end_time:
        raise serializers.ValidationError(
            "End time must be greater than start time.")


# Validator to check if start_date is less than end_date
def validate_date(self):
    if self.start_date >= self.end_date:
        raise serializers.ValidationError(
            "End date must be greater than start date.")


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'user', 'start_time', 'end_time', 'start_date',
                  'end_date', 'day', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': True},
            'start_time': {'required': True},
            'end_time': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True}
        }

        def validate(self):
            validate_time(self)
            validate_date(self)
            return self
