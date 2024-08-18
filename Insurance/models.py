
# Create your models here.
from django.db import models
import uuid
from Patient.models import Patient

class Insurance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurances')
    provider = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=255)
    coverage_details = models.TextField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Insurance for {self.patient.f_name} {self.patient.l_name} by {self.provider}"

   

