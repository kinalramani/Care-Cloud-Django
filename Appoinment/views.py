from django.shortcuts import render
# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment, Patient, Doctor
from .serializer import AppointmentSerializer

@api_view(["POST"])
def create_appointment(request):
    data = request.data
    try:
        patient = Patient.objects.get(id=data["patient"])
        doctor = Doctor.objects.get(id=data["doctor"])
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AppointmentSerializer(data=data)
    if serializer.is_valid():
        serializer.save(patient=patient, doctor=doctor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_all_appointments(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)



@api_view(["GET"])
def get_appointment_by_id(request):
    appointment_id = request.data.get("id")
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["PUT"])
def update_appointment(request):
    data = request.data
    appointment_id = data.get("id")
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AppointmentSerializer(appointment, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def delete_appointment(request):
    appointment_id = request.data.get("id")
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.is_deleted:
            return Response({"error": "Appointment already deleted"}, status=status.HTTP_400_BAD_REQUEST)
        appointment.is_deleted = True
        appointment.is_active = False
        appointment.save()
        return Response({"message": "Appointment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

