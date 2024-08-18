from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        extra_kwargs = {
            'patient': {'required': True},
            'doctor': {'required': True},
        }
