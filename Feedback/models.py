

# Create your models here.
from django.db import models
import uuid
from Patient.models import Patient
from Doctor.models import Doctor

class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField()  # Assume rating is between 1 and 5
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.patient.f_name if self.patient else 'N/A'} or Dr. {self.doctor.l_name if self.doctor else 'N/A'}: {self.content[:50]}"
