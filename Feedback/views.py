from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback
from .serializers import FeedbackSerializer

@api_view(["POST"])
def create_feedback(request):
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
def get_all_feedbacks(request):
    feedbacks = Feedback.objects.filter(is_deleted=False)
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)




@api_view(["GET"])
def get_feedback_by_id(request):
    feedback_id = request.headers.get("Feedback-ID")
    if not feedback_id:
        return Response({"detail": "Feedback-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        feedback = Feedback.objects.get(id=feedback_id, is_deleted=False)
    except Feedback.DoesNotExist:
        return Response({"detail": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = FeedbackSerializer(feedback)
    return Response(serializer.data)




@api_view(["PUT"])
def update_feedback(request):
    feedback_id = request.headers.get("Feedback-ID")
    if not feedback_id:
        return Response({"detail": "Feedback-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        feedback = Feedback.objects.get(id=feedback_id, is_deleted=False)
    except Feedback.DoesNotExist:
        return Response({"detail": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = FeedbackSerializer(feedback, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["DELETE"])
def delete_feedback(request):
    feedback_id = request.headers.get("Feedback-ID")
    if not feedback_id:
        return Response({"detail": "Feedback-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        feedback = Feedback.objects.get(id=feedback_id, is_deleted=False)
    except Feedback.DoesNotExist:
        return Response({"detail": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

    feedback.is_deleted = True
    feedback.is_active = False
    feedback.save()
    return Response({"detail": "Feedback deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
