from rest_framework import serializers
from .models import Doctor, Otp


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class OtpSerializers(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = "__all__"