from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import LabTest
from .serializers import LabTestSerializer

@api_view(["POST"])
def create_labtest(request):
    data = request.data
    serializer = LabTestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_all_labtests(request):
    labtests = LabTest.objects.filter(is_deleted=False)
    serializer = LabTestSerializer(labtests, many=True)
    return Response(serializer.data)


from django.shortcuts import get_object_or_404

@api_view(["GET"])
def get_labtest_by_id(request, id):  # Accept the id parameter here
    try:
        labtest = get_object_or_404(LabTest, id=id, is_deleted=False)
        serializer = LabTestSerializer(labtest)
        return Response(serializer.data)
    except LabTest.DoesNotExist:
        return Response({"error": "LabTest not found"}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(["PUT"])
def update_labtest(request, id):  # Accept the id parameter here
    try:
        labtest = LabTest.objects.get(id=id, is_deleted=False)
    except LabTest.DoesNotExist:
        return Response({"error": "LabTest not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LabTestSerializer(labtest, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["DELETE"])
def delete_labtest(request, id):  # Accept the id parameter here
    try:
        labtest = LabTest.objects.get(id=id, is_deleted=False)
    except LabTest.DoesNotExist:
        return Response({"error": "LabTest not found"}, status=status.HTTP_404_NOT_FOUND)

    labtest.is_deleted = True
    labtest.is_active = False
    labtest.save()

    return Response({"message": "LabTest deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
