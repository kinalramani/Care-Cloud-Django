from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Billing
from .serializers import BillingSerializer

@api_view(["POST"])
def create_billing(request):
    serializer = BillingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_all_billings(request):
    billings = Billing.objects.filter(is_deleted=False)
    serializer = BillingSerializer(billings, many=True)
    return Response(serializer.data)



@api_view(["GET"])
def get_billing_by_id(request, id):
    billing = get_object_or_404(Billing, id=id, is_deleted=False)
    serializer = BillingSerializer(billing)
    return Response(serializer.data)





@api_view(["PUT"])
def update_billing(request, id):
    billing = get_object_or_404(Billing, id=id)
    if billing.is_deleted:
        return Response({"message": "Billing is deleted"}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data
    serializer = BillingSerializer(billing, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["DELETE"])
def delete_billing(request, id):
    billing = get_object_or_404(Billing, id=id)
    if billing.is_deleted:
        return Response({"message": "Billing already deleted"}, status=status.HTTP_400_BAD_REQUEST)
    
    billing.is_deleted = True
    billing.is_active = False
    billing.save()

    return Response({"message": "Billing deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




@api_view(["GET"])
def get_billings_by_patient(request, patient_id):
    billings = Billing.objects.filter(patient_id=patient_id, is_deleted=False)
    serializer = BillingSerializer(billings, many=True)
    return Response(serializer.data)




@api_view(["GET"])
def get_billings_by_status(request, status):
    billings = Billing.objects.filter(status=status, is_deleted=False)
    serializer = BillingSerializer(billings, many=True)
    return Response(serializer.data)



@api_view(["GET"])
def get_active_billings(request):
    billings = Billing.objects.filter(is_active=True, is_deleted=False)
    serializer = BillingSerializer(billings, many=True)
    return Response(serializer.data)



@api_view(["GET"])
def get_deleted_billings(request):
    billings = Billing.objects.filter(is_deleted=True)
    serializer = BillingSerializer(billings, many=True)
    return Response(serializer.data)
