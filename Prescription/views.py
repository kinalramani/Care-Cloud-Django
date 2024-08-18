from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Prescription
from .serializers import PrescriptionSerializer

@api_view(['POST'])
def create_prescription(request):
    serializer = PrescriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['GET'])
def get_prescription(request):
    prescriptions = Prescription.objects.filter(is_active=True, is_deleted=False)
    serializer = PrescriptionSerializer(prescriptions, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_prescription_by_id(request):
    patient_id = request.headers.get('Patient-ID')
    appointment_id = request.headers.get('Appointment-ID')
    prescription = get_object_or_404(Prescription, patient_id=patient_id, appointment_id=appointment_id)
    serializer = PrescriptionSerializer(prescription)
    return Response(serializer.data)



@api_view(['PUT'])
def update_prescription(request):
    patient_id = request.headers.get('Patient-ID')
    appointment_id = request.headers.get('Appointment-ID')
    prescription = get_object_or_404(Prescription, patient_id=patient_id, appointment_id=appointment_id)
    if prescription.is_deleted or not prescription.is_active:
        return Response({"message": "Prescription cannot be updated."}, status=403)
    serializer = PrescriptionSerializer(prescription, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)




@api_view(['DELETE'])
def delete_prescription(request):
    patient_id = request.headers.get('Patient-ID')
    appointment_id = request.headers.get('Appointment-ID')
    prescription = get_object_or_404(Prescription, patient_id=patient_id, appointment_id=appointment_id)
    if prescription.is_deleted:
        return Response({"message": "Prescription already deleted."}, status=400)
    prescription.is_deleted = True
    prescription.is_active = False
    prescription.save()
    return Response({"message": "Prescription deleted successfully."}, status=204)





@api_view(['GET'])
def get_prescriptions_by_patient(request):
    patient_id = request.headers.get('Patient-ID')
    prescriptions = Prescription.objects.filter(patient_id=patient_id, is_active=True, is_deleted=False)
    serializer = PrescriptionSerializer(prescriptions, many=True)
    return Response(serializer.data)
