
from rest_framework import serializers
from .models import Patient, Otp


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = "__all__"