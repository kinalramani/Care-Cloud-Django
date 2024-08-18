
from django.db import models
import uuid
from Patient.models import Patient
from Doctor.models import Doctor
# Create your models here.



class LabTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    test_types = models.TextField()
    results = models.TextField(blank=True, null=True)
    online_results = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"LabTest for {self.patient.f_name} {self.patient.l_name} by Dr. {self.doctor.l_name} on {self.date}"

   

