from rest_framework import serializers
from .models import GeneralNote, DoctorNote


class GeneralNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralNote
        fields = ['id', 'patient', 'note', 'created_at', 'updated_at',
                  'created_by', 'updated_by']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
            'patient': {'required': True},
            'note': {'required': True}}


class DoctorNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorNote
        fields = ['id', 'patient', 'note', 'created_at', 'updated_at',
                  'created_by', 'updated_by']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
            'patient': {'required': True},
            'note': {'required': True}}
