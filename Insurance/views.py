from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Insurance
from .serializers import InsuranceSerializer

@api_view(["POST"])
def create_insurance(request):
    serializer = InsuranceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_all_insurances(request):
    insurances = Insurance.objects.filter(is_deleted=False)
    serializer = InsuranceSerializer(insurances, many=True)
    return Response(serializer.data)



@api_view(["GET"])
def get_insurance_by_id(request):
    insurance_id = request.headers.get("Insurance-ID")
    if not insurance_id:
        return Response({"detail": "Insurance-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        insurance = Insurance.objects.get(id=insurance_id, is_deleted=False)
    except Insurance.DoesNotExist:
        return Response({"detail": "Insurance not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = InsuranceSerializer(insurance)
    return Response(serializer.data)




@api_view(["PUT"])
def update_insurance(request, id):
    try:
        insurance = Insurance.objects.get(id=id)
    except Insurance.DoesNotExist:
        return Response({"error": "Insurance not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InsuranceSerializer(insurance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["DELETE"])
def delete_insurance(request, id):
    try:
        insurance = Insurance.objects.get(id=id, is_deleted=False)
    except Insurance.DoesNotExist:
        return Response({"detail": "Insurance not found."}, status=status.HTTP_404_NOT_FOUND)

    insurance.is_deleted = True
    insurance.is_active = False
    insurance.save()
    return Response({"detail": "Insurance deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




@api_view(["GET"])
def get_insurances_by_patient(request):
    patient_id = request.headers.get("Patient-ID")
    if not patient_id:
        return Response({"detail": "Patient-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)
    insurances = Insurance.objects.filter(patient_id=patient_id, is_deleted=False)
    serializer = InsuranceSerializer(insurances, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def restore_insurance(request):
    insurance_id = request.headers.get("Insurance-ID")
    if not insurance_id:
        return Response({"detail": "Insurance-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        insurance = Insurance.objects.get(id=insurance_id, is_deleted=True)
    except Insurance.DoesNotExist:
        return Response({"detail": "Insurance not found."}, status=status.HTTP_404_NOT_FOUND)
    
    insurance.is_deleted = False
    insurance.is_active = True
    insurance.save()
    return Response({"detail": "Insurance restored successfully."}, status=status.HTTP_200_OK)


